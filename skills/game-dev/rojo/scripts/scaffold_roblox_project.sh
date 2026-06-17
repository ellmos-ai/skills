#!/usr/bin/env bash
# scaffold_roblox_project.sh — legt ein Rojo-Roblox-Projektskelett an.
#
# Aufruf:
#   bash scaffold_roblox_project.sh <ProjektName> [--nested]
#
#   <ProjektName>   Verzeichnis- und Rojo-Projektname (PascalCase empfohlen)
#   --nested        verschachteltes Mapping (ReplicatedStorage.<Name>.shared statt flach)
#
# Erzeugt: default.project.json, rokit.toml, wally.toml, KONZEPT.md (Stub)
#          und src/{shared,server,client,gui}/ mit Starter-Dateien.
# Danach:  cd <ProjektName> && rokit install && rojo serve
#
# Nutzerneutral — keine festen Pfade. Reines POSIX-sh/bash.

set -euo pipefail

NAME="${1:-}"
MODE="flat"
[ "${2:-}" = "--nested" ] && MODE="nested"

if [ -z "$NAME" ]; then
  echo "Usage: bash scaffold_roblox_project.sh <ProjektName> [--nested]" >&2
  exit 1
fi
if [ -e "$NAME" ]; then
  echo "FEHLER: '$NAME' existiert bereits." >&2
  exit 2
fi

mkdir -p "$NAME"/src/{shared,server,client,gui}

# --- rokit.toml -------------------------------------------------------------
cat > "$NAME/rokit.toml" <<'EOF'
[tools]
rojo = "rojo-rbx/rojo@7.4.4"
lune = "lune-org/lune@0.10.4"
wally = "UpliftGames/wally@0.3.2"
EOF

# --- wally.toml -------------------------------------------------------------
cat > "$NAME/wally.toml" <<EOF
[package]
name = "workspace/$(echo "$NAME" | tr '[:upper:]' '[:lower:]')"
version = "0.1.0"
registry = "https://github.com/UpliftGames/wally-index"
realm = "shared"

[dependencies]
EOF

# --- default.project.json ---------------------------------------------------
if [ "$MODE" = "nested" ]; then
  cat > "$NAME/default.project.json" <<EOF
{
  "name": "$NAME",
  "tree": {
    "\$className": "DataModel",
    "ServerScriptService": {
      "\$className": "ServerScriptService",
      "$NAME": { "\$path": "src/server" }
    },
    "StarterPlayer": {
      "\$className": "StarterPlayer",
      "StarterPlayerScripts": {
        "\$className": "StarterPlayerScripts",
        "$NAME": { "\$path": "src/client" }
      }
    },
    "ReplicatedStorage": {
      "\$className": "ReplicatedStorage",
      "$NAME": {
        "\$className": "Folder",
        "shared": { "\$path": "src/shared" }
      }
    },
    "StarterGui": {
      "\$className": "StarterGui",
      "$NAME": { "\$path": "src/gui" }
    },
    "ServerStorage": { "\$className": "ServerStorage" },
    "Workspace": { "\$className": "Workspace" },
    "Lighting": { "\$className": "Lighting" },
    "SoundService": { "\$className": "SoundService" }
  }
}
EOF
  SHARED_PATH="ReplicatedStorage:WaitForChild(\"$NAME\"):WaitForChild(\"shared\")"
else
  cat > "$NAME/default.project.json" <<EOF
{
  "name": "$NAME",
  "tree": {
    "\$className": "DataModel",
    "ServerScriptService": { "\$className": "ServerScriptService", "\$path": "src/server" },
    "StarterPlayer": {
      "\$className": "StarterPlayer",
      "StarterPlayerScripts": { "\$className": "StarterPlayerScripts", "\$path": "src/client" }
    },
    "ReplicatedStorage": { "\$className": "ReplicatedStorage", "\$path": "src/shared" },
    "StarterGui": { "\$className": "StarterGui", "\$path": "src/gui" },
    "ServerStorage": { "\$className": "ServerStorage" },
    "Workspace": { "\$className": "Workspace" },
    "Lighting": { "\$className": "Lighting" },
    "SoundService": { "\$className": "SoundService" }
  }
}
EOF
  SHARED_PATH="ReplicatedStorage"
fi

# --- src/shared -------------------------------------------------------------
cat > "$NAME/src/shared/Config.luau" <<'EOF'
--!strict
-- Config: zentrale Gameplay-Werte und States. Eine Quelle der Wahrheit.
local Config = {}

Config.States = {
	LOBBY = "Lobby",
	PLAYING = "Playing",
	ENDED = "Ended",
}

Config.RoundSeconds = 120

return Config
EOF

cat > "$NAME/src/shared/GameEnums.luau" <<'EOF'
--!strict
-- GameEnums: Remote-Namen und Enums zentral. Server erstellt + Client sucht über dieselben Namen.
local GameEnums = {}

GameEnums.Remotes = {
	GAME_STATE = "GameStateChanged",
	INTERACT = "InteractRequest",
}

return GameEnums
EOF

# --- src/server -------------------------------------------------------------
cat > "$NAME/src/server/Main.server.luau" <<EOF
--!strict
-- Main: EINZIGER Server-Entry-Point. Erstellt Remotes, required Manager-Module.
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local shared = $SHARED_PATH

local Config = require(shared:WaitForChild("Config"))
local GameEnums = require(shared:WaitForChild("GameEnums"))

-- Remotes-Ordner zentral hier anlegen, BEVOR andere Scripts laufen.
local remotes = Instance.new("Folder")
remotes.Name = "Remotes"
remotes.Parent = ReplicatedStorage

for _, remoteName in GameEnums.Remotes do
	local ev = Instance.new("RemoteEvent")
	ev.Name = remoteName
	ev.Parent = remotes
end

print("[$NAME] Server gestartet. State:", Config.States.LOBBY)
EOF

# --- src/client -------------------------------------------------------------
cat > "$NAME/src/client/GameClient.client.luau" <<EOF
--!strict
-- GameClient: Client-Entry-Point. Schreibt geteilten State, hört auf Server-Events.
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local shared = $SHARED_PATH

local Config = require(shared:WaitForChild("Config"))

_G.ClientState = {
	gameState = Config.States.LOBBY,
}

local remotes = ReplicatedStorage:WaitForChild("Remotes")
print("[$NAME] Client bereit. Remotes:", remotes:GetChildren())
EOF

# --- src/gui ----------------------------------------------------------------
cat > "$NAME/src/gui/HUD.client.luau" <<EOF
--!strict
-- HUD: baut die GUI auf und liest _G.ClientState im Heartbeat.
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")

local gui = Instance.new("ScreenGui")
gui.Name = "${NAME}HUD"
gui.ResetOnSpawn = false
gui.Parent = Players.LocalPlayer:WaitForChild("PlayerGui")

local label = Instance.new("TextLabel")
label.Size = UDim2.new(0, 200, 0, 30)
label.Position = UDim2.new(0, 10, 0, 10)
label.BackgroundTransparency = 0.4
label.Parent = gui

RunService.Heartbeat:Connect(function()
	local cs = _G.ClientState
	if not cs then return end
	label.Text = "State: " .. tostring(cs.gameState)
end)
EOF

# --- KONZEPT.md -------------------------------------------------------------
cat > "$NAME/KONZEPT.md" <<EOF
# $NAME — KONZEPT (Game Design Document)

## Vision
<1–2 Sätze: Was ist das Spiel?>

## Genre / Vorbild
<z. B. Sci-Fi Base Builder, Vorbild Clash of Clans>

## Kern-Mechaniken (max. 3–4)
1.
2.
3.

## Monetarisierung
<Gamepasses, Developer Products, Battle Pass, …>

## Technik
- Rojo / rokit (siehe rokit.toml), Mapping: $MODE

## Nächste Schritte
- [ ] Backend (Config → GameEnums → Defs → Main → Manager)
- [ ] Frontend (GameClient → HUD)
- [ ] Playtest
EOF

echo "OK: Projekt '$NAME' angelegt (Mapping: $MODE)."
echo "Nächste Schritte:"
echo "  cd $NAME && rokit install && rojo serve"
