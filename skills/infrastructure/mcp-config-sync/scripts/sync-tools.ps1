# sync-tools.ps1
# Synchronisiert MCP-Server zwischen Claude Code und Claude Desktop.
# Master: %USERPROFILE%\.claude\_shared-mcp.json
# Ziel 1: %USERPROFILE%\.claude\profiles\shared.json    (Claude Code)
# Ziel 2: %APPDATA%\Claude\claude_desktop_config.json   (Claude Desktop, mergen)
#
# Aufruf:
#   powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.claude\sync-tools.ps1"
#
# Stand: 2026-06-13

$ErrorActionPreference = 'Stop'

$master = Join-Path $env:USERPROFILE '.claude\_shared-mcp.json'
$ccProfile = Join-Path $env:USERPROFILE '.claude\profiles\shared.json'
$cdConfig = Join-Path $env:APPDATA 'Claude\claude_desktop_config.json'

if (-not (Test-Path $master)) { Write-Error "Master fehlt: $master"; exit 1 }
$m = Get-Content $master -Raw | ConvertFrom-Json
if (-not $m.mcpServers) { Write-Error 'Master hat keinen mcpServers-Block'; exit 1 }

# --- Ziel 1: Claude-Code-Profile shared.json ---
$cc = [ordered]@{ mcpServers = $m.mcpServers }
$cc | ConvertTo-Json -Depth 10 | Set-Content -Path $ccProfile -Encoding UTF8
Write-Host "[OK] Claude Code profile geschrieben: $ccProfile"

# --- Ziel 2: Claude-Desktop-Config mergen ---
if (Test-Path $cdConfig) {
    $cd = Get-Content $cdConfig -Raw | ConvertFrom-Json
} else {
    $cd = [PSCustomObject]@{}
}

$cd | Add-Member -NotePropertyName 'mcpServers' -NotePropertyValue $m.mcpServers -Force

$backup = "$cdConfig.backup-$(Get-Date -Format yyyyMMdd-HHmmss)"
if (Test-Path $cdConfig) {
    Copy-Item $cdConfig $backup -Force
    Write-Host "[OK] Backup: $backup"
}

$cd | ConvertTo-Json -Depth 10 | Set-Content -Path $cdConfig -Encoding UTF8
Write-Host "[OK] Claude Desktop config geschrieben: $cdConfig"

Write-Host ''
Write-Host '=== Sync abgeschlossen ==='
Write-Host 'Naechster Schritt:'
Write-Host '  - Claude Desktop komplett beenden (Tray-Icon -> Quit) und neu starten'
Write-Host '  - In Claude Code: claude --mcp-config ~/.claude/profiles/shared.json'
