---
name: github-repo-care
version: 1.0.0
type: protocol
author: Lukas Geiger + Codex
created: 2026-06-18
updated: 2026-06-18
aliases: [github-pflege, repo-veroeffentlichen, repo-release, privacy-gate, release-gate]
description: Protocolo para crear, publicar, lanzar, auditar y mantener repositorios de GitHub de forma segura: verificar reglas locales y bloqueos, crear .gitignore antes del primer git add, realizar verificaciones de privacidad, preparar README/i18n/banner/metadatos, verificar etiquetas de release y lanzamientos de GitHub, y actualizar perfiles de organización, archivos llms.txt y enlaces a registros.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [github, repo, release, privacy, i18n, marketing, ci, documentation]
language: es
status: active
dependencies: {'tools': ['git', 'gh', 'rg'], 'services': ['GitHub'], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.codex/skills/github-repo-care/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': '2026-06-18', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="github-repo-care banner">

> **Español** — Versión oficial en español de `github-repo-care`.


# GitHub Repo Care — Publicar y mantener repositorios de forma limpia (Español)

## Cuándo usar

Usa esta habilidad cuando necesites crear, publicar, lanzar, auditar o mantener un repositorio de GitHub. Es especialmente importante antes del primer push público, para etiquetas de release, metadatos del repositorio, perfiles de organización y verificaciones de privacidad.

No la utilices para tareas de implementación pura que no requieran un paso de publicación en GitHub. Finaliza primero el flujo de trabajo de desarrollo o depuración pertinente y luego activa esta habilidad para la publicación.

## Regla principal

Prepara el repositorio antes del primer push público. Un `.gitignore` correcto, un control de privacidad (privacy gate), licencia, README, metadatos e historial de lanzamientos resultan mucho más económicos antes de que exista un historial público.

## Flujo de trabajo y procedimiento

1. **Leer las reglas locales.** Consulta `AGENTS.md`, `CLAUDE.md`, `START.md`, política de releases, política de nombres y política de bloqueos si están presentes.
2. **Verificar bloqueos.** Si `LOCK.txt` o un `LOCK.*.txt` coincidente está activo, no edites ese alcance.
3. **Fijar la identidad del repositorio.** Confirma el nombre, organización, visibilidad, licencia y el propósito en una sola frase.
4. **Crear `.gitignore` antes de `git add`.** Excluye secretos, datos locales, bases de datos, salida de compilación, entornos virtuales, cachés, archivos de IDE y notas privadas.
5. **Añadir los elementos públicos básicos.** Archivos típicos: `README.md`, `LICENSE`, `CHANGELOG.md`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `llms.txt` y CI.
6. **Redactar el README para la visibilidad.** Primer área visible: propósito, instalación, uso, modelo de privacidad, estructura del proyecto, licencia y nombre canónico del repositorio.
7. **Añadir elementos visuales.** Incluye un banner, logotipo o captura de pantalla cuando facilite la comprensión del proyecto. Evita la decoración genérica si es posible incluir una imagen real del producto o un esquema conceptual claro.
8. **Planificar i18n deliberadamente.** Mínimo: inglés más el idioma del proyecto. Conjunto estándar preferido para módulos orientados al usuario: alemán, inglés, español, chino simplificado, japonés y ruso.
9. **Ejecutar pruebas y comprobaciones iniciales (smokes).** Verifica localmente antes de confirmar el éxito o crear un release.
10. **Ejecutar el control de privacidad (privacy gate).** Revisa el conjunto preparado (staged/tracked) en busca de secretos, rutas locales, datos personales (PII), `.env`, bases de datos, documentos privados, artefactos generados y caracteres corruptos (mojibake).
11. **Hacer commit y push.** Realiza el commit solo después de superar el control. A continuación, crea o conecta el repositorio de GitHub, haz push y verifica el estado remoto.
12. **Establecer los metadatos.** Revisa la descripción, etiquetas (topics), página principal, visibilidad y rama predeterminada.
13. **Crear el release.** Crea la etiqueta (tag) y el lanzamiento en GitHub (GitHub release); verifica CI tanto para la rama como para el tag.
14. **Actualizar las superficies de descubrimiento.** Añade enlaces desde el perfil de la organización, `llms.txt`, registros centrales, índices de módulos locales y READMEs del ecosistema.
15. **Verificación final.** Revisa el README remoto, la página de releases, los topics, CI y los enlaces.

## Control de privacidad (Privacy Gate)

Busca en el conjunto preparado o rastreado (staged/tracked), no solo en el árbol de trabajo visible.

```bash
git diff --cached --check
git ls-files
rg -n "C:\\\\Us[e]rs\\\\|C:/Us[e]rs/|/c/Us[e]rs/|s[k]-[A-Za-z0-9]|gh[p]_|gh[o]_|API[_-]?KEY|TO[K]EN|PASS[W]ORD|SEC[R]ET|\\x{C3}|\\x{C2}|\\x{FFFD}" .
```

Para módulos públicos, documenta también un `RELEASE_GATE.md` o un registro equivalente: fecha, comandos ejecutados, resultado, advertencias pendientes y excepciones intencionadas. Si alguna vez se envió un secreto al repositorio, eliminarlo de `HEAD` no es suficiente; debes rotar el secreto.

## Metadatos de GitHub

Después del push, configura explícitamente los metadatos y los datos del release.

```bash
gh repo edit ORG/REPO --description "Short concrete description" \
  --add-topic local-first --add-topic python --add-topic llm
git tag -a v1.0.0 -m "v1.0.0"
git push origin v1.0.0
gh release create v1.0.0 --repo ORG/REPO --title "v1.0.0" --notes "..."
```

A continuación, verifica:

```bash
gh repo view ORG/REPO --json nameWithOwner,visibility,description,repositoryTopics,url
gh release view v1.0.0 --repo ORG/REPO --json tagName,url,isDraft,isPrerelease
gh run list --repo ORG/REPO --limit 5
```

Si el CI se muestra en rojo después de un release, el repositorio aún no se ha publicado limpiamente. Para un lanzamiento inicial recién creado, es aceptable mover de forma inmediata e intencionada la etiqueta recién creada al commit corregido.

## Errores comunes

| Error | Solución |
|---|---|
| Se añade `.gitignore` después de `git add` | Sacar del área de preparación (unstage) primero, corregir las reglas de ignore y volver a añadir |
| El README es monolingüe aunque la interfaz o habilidad sea multilingüe | Añadir enlaces de idiomas o READMEs localizados |
| No hay banner, topics ni descripción | Añadir elementos de descubrimiento antes del anuncio |
| La etiqueta de release existe, pero el CI está en rojo | Corregir el CI y verificar la nueva ejecución |
| Se actualiza el README de la organización, pero se omite `llms.txt` | Actualizar tanto las superficies para humanos como para máquinas |
| Aparece una ruta local en la documentación pública | Reemplazarla por rutas relativas o ejemplos genéricos |
| El repositorio público contiene una base de datos de pruebas o bandeja de entrada de notebooks | Eliminarlo del seguimiento, añadir reglas de ignore y volver a ejecutar el control |

## Lista de comprobación final

- [ ] Reglas locales y bloqueos verificados.
- [ ] `.gitignore` existía antes del primer add.
- [ ] Documentación pública, licencia, seguridad, contribución, changelog y `llms.txt` presentes.
- [ ] README incluye nombre del repositorio, propósito, instalación, uso, privacidad y licencia.
- [ ] Expectativa de i18n cumplida.
- [ ] Banner, logotipo o captura de pantalla presente cuando resulte útil.
- [ ] Pruebas y verificaciones iniciales (smokes) superadas.
- [ ] Análisis de privacidad, rutas, secretos, bases de datos y mojibake limpios.
- [ ] Descripción de GitHub, topics, etiqueta (tag), release y CI verificados.
- [ ] Perfil de la organización, registros y enlaces del ecosistema actualizados.

## Historial de cambios

### 1.0.0 (2026-06-18)
- Creado el protocolo inicial de mantenimiento y publicación de repositorios.
