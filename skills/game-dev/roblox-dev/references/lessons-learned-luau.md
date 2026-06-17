# Luau- & Roblox-Lessons-Learned

Empirisch gesammelte Fallstricke aus realer Roblox-Entwicklung. Nach Kategorie geordnet.

---

## Syntax & Operatoren

- **Semicolon nach `task.wait()`:** `task.wait(1); n:Destroy()` — ohne `;` interpretiert Luau die
  Folgezeile als Funktionsaufruf auf den Rückgabewert: `task.wait(1)(n:Destroy())`.
- **`Model.Position` existiert nicht:** `model:GetPivot().Position` oder `model.PrimaryPart.Position`.
- **`#table` auf Dictionaries = 0:** `#` gilt nur für Arrays. Dict-Länge manuell zählen:
  `local n = 0; for _ in dict do n += 1 end`.
- **`mouse.Hit` kann nil sein:** vor Gebrauch prüfen — `if not mouse.Hit then return end`.
- **CFrame + Vector3 ist ungültig:** `cf * CFrame.new(dx, dy, dz)` statt `cf + Vector3.new(...)`.
- **Operator-Präzedenz bei Concatenation:** `..` bindet stärker als `+` → Arithmetik klammern:
  `"XP: " .. (baseXP + bonus)`.

## Luau-Sprachgrenzen

- **200-Local-Register-Limit:** Sehr große Scripts (~195+ module-scope locals) brechen. Neue
  Features in `do ... end`-Blöcke kapseln, statt weitere top-level locals anzulegen.

## Deprecated / falsche Roblox-API

- **`tick()`** → deprecated. `os.clock()` (Monotonic) oder `workspace:GetServerTimeNow()`.
- **`SetPrimaryPartCFrame()`** → deprecated. `model:PivotTo(cf)`.
- **`GetTouchingParts()`** → unzuverlässig. `workspace:GetPartsInPart(part)`.
- **`Enum.Material.Rope`** existiert nicht → `Enum.Material.Fabric`.
- **`Lighting.Technology`** lässt sich nicht zur Laufzeit setzen (braucht RobloxScript-Capability).

## DataStore & Networking

- **DataStore immer mit `pcall`:** `local ok, data = pcall(function() return store:GetAsync(key) end)`.
- **RemoteEvents zentral & früh:** alle Remotes in `Main.server.luau` erstellen, **bevor** andere
  Scripts laufen. Sonst hängt der Client in `WaitForChild()` (Deadlock).
- **Event-Namen zentralisieren:** in `GameEnums.Remotes` definieren; Server erstellt + Client sucht
  über dieselben Konstanten → keine String-Mismatches.

## Architektur-Fallen

- **Zirkuläre Requires** (A require B, B require A) → Deadlock. Lazy lösen:
  `task.spawn(function() task.wait(); Other = require(OtherModule) end)`.
- **`.server.luau` vs. `.luau`:** Entry-Point ist `.server.luau`/`.client.luau`; alle per
  `require()` geladenen Module sind `.luau`-ModuleScripts.
- **`.rbxl` + Rojo gefährlich:** Rojo überschreibt gemappte Bereiche beim Connect. Assets in eine
  **scriptfreie** `.rbxl` legen, Code ausschließlich in `src/`.

## Studio / MCP-Besonderheiten

- **MCP-`require()`-Cache:** Der Plugin-VM hat einen eigenen require-Cache. Zur Wert-Verifikation
  `.Source` direkt lesen oder Server-Logs nach Play-Start prüfen, nicht dem Cache vertrauen.
- **MCP-Edits sind nicht persistent:** per MCP geschriebene Scripts verschwinden nach Play/Stop —
  für bleibende Code-Änderungen Rojo nutzen.
- **`multi_edit`-Workaround:** Wenn Rojos File-Watcher sehr große Änderungen (>150 KB) nicht
  erkennt, gezielt `multi_edit` einsetzen.

## Welt & Performance

- **Z-Fighting:** Baseplate und prozeduraler Boden auf gleicher Höhe → Flackern. Baseplate
  entfernen oder Boden +0.1 Studs anheben.
- **Part-Budget:** ~50–80 Parts pro prozedural generiertem Raum als Richtwert.
- **CollectionService statt manueller Listen:** `CollectionService:GetTagged("Hazard")` +
  `GetInstanceAddedSignal()` statt selbstgepflegter Tabellen.
