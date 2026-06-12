#!/usr/bin/env bash
# sync-tools.sh — macOS-Variante
# Synchronisiert MCP-Server zwischen Claude Code und Claude Desktop.
# Master: ~/.claude/_shared-mcp.json
# Ziel 1: ~/.claude/profiles/shared.json
# Ziel 2: ~/Library/Application Support/Claude/claude_desktop_config.json
#
# Voraussetzung: jq (brew install jq)
# Stand: 2026-04-30

set -euo pipefail

MASTER="$HOME/.claude/_shared-mcp.json"
CC_PROFILE="$HOME/.claude/profiles/shared.json"
CD_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

if [ ! -f "$MASTER" ]; then
    echo "Master fehlt: $MASTER" >&2
    exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
    echo "jq fehlt. Installation: brew install jq" >&2
    exit 1
fi

# --- Ziel 1: Claude-Code-Profile ---
mkdir -p "$(dirname "$CC_PROFILE")"
jq '{ mcpServers: .mcpServers }' "$MASTER" > "$CC_PROFILE"
echo "[OK] Claude Code profile -> $CC_PROFILE"

# --- Ziel 2: Claude-Desktop-Config (mergen) ---
mkdir -p "$(dirname "$CD_CONFIG")"

if [ -f "$CD_CONFIG" ]; then
    BACKUP="${CD_CONFIG}.backup-$(date +%Y%m%d-%H%M%S)"
    cp "$CD_CONFIG" "$BACKUP"
    echo "[OK] Backup -> $BACKUP"
    jq --slurpfile master "$MASTER" '.mcpServers = $master[0].mcpServers' "$CD_CONFIG" > "${CD_CONFIG}.tmp"
    mv "${CD_CONFIG}.tmp" "$CD_CONFIG"
else
    jq '{ mcpServers: .mcpServers }' "$MASTER" > "$CD_CONFIG"
fi
echo "[OK] Claude Desktop config -> $CD_CONFIG"

echo ""
echo "=== Sync abgeschlossen ==="
echo "Naechster Schritt:"
echo "  - Claude Desktop komplett beenden (Cmd+Q) und neu starten"
echo "  - In Claude Code: claude --mcp-config ~/.claude/profiles/shared.json"
