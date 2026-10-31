---
name: protection-shield
version: 1.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-10-25
updated: 2026-10-25
description: "Coordina defensa inmediata autorizada y revisiones periódicas de registros y versiones con pruebas y reversión."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [defense, incident-response, server, logs, monitoring]
language: es
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [tech-detect, security-tech-stack-check], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# protection-shield

Solo para sistemas, redes o servidores propios o autorizados. Antes de cambiar producción comprobar activo, propietario, autoridad, bloqueos, impacto y reversión. Una alerta no concede permiso. Prohibidos contraataques, acceso a activos ajenos y exploraciones no autorizadas.

En una urgencia, conservar UTC, registros pertinentes limitados y hash de configuración; ocultar secretos y separar síntomas de compromiso confirmado. Leer runbook, decisiones vigentes y acción privada por activo. Si existe autoridad concreta, usar herramientas nativas para el servicio, regla de firewall, rotación aprobada o parche mediante security-tech-stack-check. Vincular objetivo y restauración; verificar salida, funcionamiento, efecto y consecuencias. Medir la reversión por separado.

Para vigilancia periódica, un perfil privado define activos, lectores de logs/API autorizados, ventana, filtros, retención, instantánea tech-detect, calendario y destino de alertas. Conectar al programador existente, sin crear otro servicio. Cada ejecución limita fuentes y tiempo, deduplica y consulta avisos actuales mediante security-tech-stack-check. Informar cobertura y errores. Solo un recibo real del programador y del resultado demuestra que funciona.

Para la revisión periódica del mismo servidor, comparar las capturas anterior y actual con slot y hostname sin cambios mediante tech-detect compare. Comprobar axis=same-host-time, chronology, ambas horas, cobertura y versiones inciertas. No renombrar el equipo para que pase la comparación; si falta procedencia, HOLD.
