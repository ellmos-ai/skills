---
name: backup
version: 1.0.0
type: skill
author: User
created: 2026-08-24
updated: 2026-08-24
description: "Plant, refleja, verifica, restaura o archiva archivos de forma explícita mediante el núcleo mac-backup con parada segura (fail-closed). Usar para los trabajos de copia de seguridad entre hosts propios del usuario; no para sincronización general en la nube ni para copias de archivos casuales."
visibility: public
language: es
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
provenance:
  origin: "custom"
  origin_repo: "github.com/ellmos-ai/mac-backup"
  last_sync_from_origin: "2026-08-24"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: c50a9f8b557b5e4baa08f880f28ba234c8f56974e644ce57147bde5311a02ad6
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.065724+00:00"
---
<img src="banner.png" width="100%" alt="backup banner">

# Backup

Usar la CLI instalada de `mac-backup` como única implementación de transferencia. No reconstruir el flujo
con `scp`, `rsync`, SSHFS, acciones del Explorador ni eliminación ad hoc.

## Enrutar la solicitud

- Una solicitud ordinaria de "backup" significa `mirror`; el origen permanece intacto.
- `archive` significa limpieza del origen y es una intención destructiva independiente. Nunca inferirla
  de "backup" (copia de seguridad), "copy" (copiar) o "free some space" (liberar espacio).
- `restore` escribe en un destino nuevo y nunca sobrescribe en silencio.
- Si no existe un JSON de trabajo verificado, preparar una propuesta de trabajo y detenerse antes de `init-target` o
  de la transferencia.

## Ejecución

1. Leer el trabajo y ejecutar `mac-backup plan <job> --json`.
2. Comprobar que la clase de origen devuelta, el número de archivos, el número de bytes, el ID del volumen de destino,
   el estado de cifrado y la huella del host coinciden con la solicitud y con la evidencia actual del dispositivo.
3. Para Mirror, ejecutar `mac-backup mirror <job> --json` y después `mac-backup verify <job> --json`.
4. Para Restore, usar un destino nuevo y absoluto, y verificar los archivos restaurados mediante el resultado
   del manifiesto del comando.
5. Para Archive, pasar `--confirm-delete` solo si el usuario pidió explícitamente la eliminación del origen y el plan
   verificado nombra exactamente ese origen. Un bloqueo de política es el resultado correcto; nunca eludir
   `target_encryption_required`, `source_class_unknown_cleanup_blocked`, `onedrive_dehydrate_not_implemented`, un lock (bloqueo de archivo/concurrencia), una discrepancia de identidad
   ni un ancla ausente.

`init-target` es configuración privilegiada, no una ejecución rutinaria. Requiere una evidencia del sistema operativo
obtenida de forma independiente para el ID del volumen y el cifrado; un valor copiado de la propuesta de trabajo no es evidencia.

Nunca afirmar que un mirror es una copia de seguridad completa antes de que la verificación del destino y una
prueba real de restauración hayan pasado ambas. Mantener fuera los secretos, los archivos de trabajo reales, los anclajes
locales y los nombres de archivo del usuario procedentes de tickets, Git y OneDrive.

## Changelog

### 1.0.0 (2026-08-24)
- Copia neutralizada del master de despliegue de `~/.claude/skills/backup/`, incorporada a la biblioteca
  categorizada. Causa de la brecha de sincronización: la skill estaba desplegada, pero no tenía una entrada de origen en `skills/<category>/`,
  por lo que `skill_sync.py status` la informaba como `NUR-ZIEL` (solo destino) y `catalog.py`/`build_public_registry.py` (que solo escanean `skills/`)
  nunca la veían; por eso nunca pudo alcanzar el registro público ni `SKILLS-MAP.md`, sin importar
  cómo se editara la copia de despliegue.
