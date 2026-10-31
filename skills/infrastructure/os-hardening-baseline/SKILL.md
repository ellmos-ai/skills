---
name: os-hardening-baseline
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: >
  Prüfliste für die Grundabsicherung eines eigenen Laptops oder PCs unter Windows, macOS
  und Linux: Updates, Schutzprogramm, Firewall, Festplattenverschlüsselung, Konten und
  Rechte, Fernzugänge, Startkette. Je Punkt eine schreibgeschützte Prüfung und ein Soll;
  Änderungen nur nach Backup und einzelner Bestätigung. Defensiv, für den Privatgebrauch
  gedacht, kein Ersatz für Vorgaben einer verwaltenden IT.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [hardening, baseline, checklist, windows, macos, linux, endpoint, defensive, security]
language: de
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: custom
  origin_path: "skills/infrastructure/os-hardening-baseline/"
  origin_version: "1.0.0"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# os-hardening-baseline (Deutsch)

Eine Grundabsicherung für ein **eigenes** Gerät, nach einem Vorfall oder vorbeugend. Die
Liste ist ein Ziel, kein Befehl: Jede Änderung wird erklärt, vorher gesichert und einzeln
bestätigt. Strukturelle Härtung ganzer Software-Projekte gehört nicht hierher, sondern zu
`sec-hardening`.

**Vorgehen:** erst nur prüfen (alle Prüfbefehle lesen nur), Abweichungen in `incident-notes`
oder einer Fallnotiz sammeln, danach mit der Eigentümerin oder dem Eigentümer entscheiden,
was geändert wird. Manche Befehle brauchen Administratorrechte; die Rechte nur für die
einzelne Prüfung nutzen. Geräte, die eine Firma oder Schule verwaltet, nicht verändern.

## Windows

| Punkt | Prüfung (lesend) | Soll |
|---|---|---|
| Updates | Einstellungen, Windows Update; `Get-HotFix` | aktuell, automatische Updates an |
| Schutzprogramm | `Get-MpComputerStatus` (Felder `AntivirusEnabled`, `RealTimeProtectionEnabled`) | aktiv, Signaturen aktuell |
| Firewall | `Get-NetFirewallProfile \| Select Name, Enabled` | alle Profile an |
| Laufwerksverschlüsselung | `Get-BitLockerVolume` (Administrator) bzw. Einstellungen | Systemlaufwerk verschlüsselt (sofern das Gerät es unterstützt), Wiederherstellungsschlüssel sicher und **nicht** auf dem Gerät aufbewahrt |
| Sicherer Start | `Confirm-SecureBootUEFI` | `True` |
| Benutzerkontensteuerung | Einstellungen, Benutzerkonten | an |
| Konten und Rechte | `Get-LocalGroupMember Administrators`, `Get-LocalUser` | Alltagskonto ohne Administratorrechte; keine unbekannten Konten; Gastkonto aus |
| Fernzugänge | Einstellungen, Remotedesktop; Fernwartungsprogramme in der Softwareliste | nur an, wenn benötigt; unbekannte Fernwartungssoftware entfernen (nach Rücksprache) |
| Veraltetes | `Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol` | SMB1 deaktiviert |
| Autostart und Aufgaben | Aufgaben-Manager, `Get-ScheduledTask` | nur bekannte Einträge |

## macOS

| Punkt | Prüfung (lesend) | Soll |
|---|---|---|
| Updates | `softwareupdate -l` | keine ausstehenden Sicherheitsupdates |
| Festplattenverschlüsselung | `fdesetup status` | FileVault an, Wiederherstellungsschlüssel sicher aufbewahrt |
| Gatekeeper | `spctl --status` | aktiviert |
| Systemintegritätsschutz | `csrutil status` | enabled |
| Firewall | `/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate` | an |
| Konten | Systemeinstellungen, Benutzer & Gruppen; `dscl . list /Users` | Alltagskonto ohne Administratorrechte; Gastkonto aus |
| Fernzugänge | Systemeinstellungen, Teilen (Entfernte Anmeldung, Bildschirmfreigabe) | nur an, wenn benötigt |
| Anmeldeobjekte und Profile | Systemeinstellungen, Allgemein, Anmeldeobjekte; Profile | nur bekannte Einträge |

## Linux

| Punkt | Prüfung (lesend) | Soll |
|---|---|---|
| Updates | `apt list --upgradable` bzw. `dnf check-update` | keine ausstehenden Sicherheitsupdates; automatische Sicherheitsupdates an |
| Firewall | `ufw status` bzw. `firewall-cmd --state` bzw. `nft list ruleset` | aktiv, eingehend standardmäßig verweigert |
| Lauschende Dienste | `ss -tulpn` | nur Erwartetes |
| SSH (falls Server läuft) | `sshd -T \| grep -E 'permitrootlogin\|passwordauthentication'` | Root-Anmeldung aus, Schlüssel statt Passwort |
| Verschlüsselung | `lsblk -f` (Typ `crypto_LUKS`) | Systemplatte bzw. Daten verschlüsselt |
| Rechte | `getent group sudo` bzw. `wheel` | nur nötige Konten |
| Startkette | Secure Boot, falls unterstützt (`mokutil --sb-state`) | an |
| Auditwerkzeug | ein anerkanntes Härtungsaudit (z. B. Lynis, lesender Modus) | Hinweise sichten, nicht blind umsetzen |

## Alle Systeme

- **Wiederherstellung:** regelmäßiges Backup auf ein Medium, das nicht dauernd verbunden ist;
  Wiederherstellung wenigstens einmal ausprobieren.
- **Konten:** Passwortmanager, einmalige lange Passwörter, Zwei-Faktor-Verfahren mit App oder
  Sicherheitsschlüssel, Wiederherstellungsangaben aktuell.
- **Software:** nur aus offiziellen Quellen; Unnötiges deinstallieren; Browser-Erweiterungen
  auf das Nötige beschränken. Installierte Software gegen aktuelle Herstellerhinweise
  gleichen: `security-tech-stack-check`.
- **Netz:** Router-Firmware aktuell, Standardkennwörter geändert, Fernzugang des Routers aus,
  wenn nicht benötigt.
- **Alltag:** Bildschirmsperre mit kurzer Frist, kein dauerhafter Administratorgebrauch,
  Skepsis bei Anhängen und Links.

## Ausführen von Änderungen

Pro Änderung: Zustand notieren, Backup bestätigt, Änderung erklärt, Eigentümerin oder
Eigentümer bestätigt einzeln, Änderung durchführen, Ergebnis erneut lesen (Prüfbefehl
wiederholen), Rückweg notieren. Keine Änderung, die Daten unlesbar machen kann
(Verschlüsselung einschalten, Partitionen ändern), ohne geprüftes Backup und gesicherten
Wiederherstellungsschlüssel.
