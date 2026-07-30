---
name: github-repo-care
version: 1.0.0
type: protocol
author: Lukas Geiger + Codex
created: 2026-06-18
updated: 2026-06-18
aliases: [github-pflege, repo-veroeffentlichen, repo-release, privacy-gate, release-gate]
description: Protocolo para crear, publicar, lanzar, auditar y mantener repositorios de GitHub de forma segura: verificar reglas y bloqueos locales, crear .gitignore antes del primer add, realizar comprobaciones de privacidad, preparar README/i18n/banner/metadatos, verificar etiquetas de lanzamiento y publicaciones de GitHub, y actualizar perfiles de organización, archivos llms.txt y enlaces de registro.
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

> **Español** — Versión oficial en español de `github-repo-care`.


# GitHub Repo Care — Publicar y mantener repositorios de forma limpia (Español)

## Cuándo usar

Usa este skill cuando necesites crear, publicar, lanzar, auditar o mantener un repositorio de GitHub. Es especialmente importante antes del primer push público, para etiquetas de lanzamiento, metadatos del repositorio, perfiles de organización y comprobaciones de privacidad.

No lo uses para trabajo de implementación puro sin un paso de publicación en GitHub. Finaliza primero el flujo de desarrollo o depuración relevante y luego activa este skill para la publicación.

## Regla fundamental

Prepara el repositorio antes del primer push público. Un `.gitignore` correcto, puerta de privacidad, licencia, README, metadatos e historial de lanzamientos son mucho más económicos antes de que exista un historial público.

## Flujo de trabajo y procedimiento

1. **Leer reglas locales.** Consulta `AGENTS.md`, `CLAUDE.md`, `START.md`, política de lanzamientos, política de nombres y política de bloqueos si están presentes.
2. **Comprobar bloqueos.** Si `LOCK.txt` o un `LOCK.*.txt` coincidente está activo, no edites ese ámbito.
3. **Fijar la identidad del repositorio.** Confirma el nombre, la organización, la visibilidad, la licencia y el propósito en una sola frase.
4. **Crear `.gitignore` antes de `git add`.** Excluye secretos, datos locales, bases de datos, salidas de compilación, entornos virtuales, cachés, archivos de IDE y notas privadas.
5. **Añadir elementos públicos básicos.** Archivos típicos: `README.md`, `LICENSE`, `CHANGELOG.md`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `llms.txt` y CI.
6. **Escribir el README para el descubrimiento.** Primer vistazo: propósito, instalación, uso, modelo de privacidad, estructura del proyecto, licencia y nombre canónico del repositorio.
7. **Añadir señales visuales.** Añade un banner, logo o captura de pantalla cuando facilite la comprensión del proyecto. Evita la decoración genérica cuando sea posible mostrar una imagen real del producto o un diagrama conceptual claro.
8. **Planificar i18n deliberadamente.** Mínimo: inglés más el idioma del proyecto. Conjunto estándar preferido para módulos orientados al usuario: alemán, inglés, español, chino simplificado, japonés y ruso.
9. **Ejecutar pruebas y comprobaciones de humo.** Verifica localmente antes de declarar éxito o crear un lanzamiento.
10. **Ejecutar la puerta de privacidad.** Inspecciona el conjunto preparado/rastreado en busca de secretos, rutas locales, PII, `.env`, bases de datos, documentos privados, artefactos generados y mojibake.
11. **Hacer commit y push.** Haz commit solo después de superar la puerta de privacidad. Luego crea o conecta el repositorio de GitHub, haz push y verifica el estado remoto.
12. **Establecer metadatos.** Revisa la descripción, temas (topics), página de inicio, visibilidad y rama por defecto.
13. **Crear el lanzamiento.** Crea la etiqueta y el lanzamiento de GitHub (GitHub release); verifica la CI tanto para la rama como para la etiqueta.
14. **Actualizar superficies de descubrimiento.** Enlaza desde el perfil de la organización, `llms.txt`, registros centrales, índices de módulos locales y READMEs del ecosistema.
15. **Verificación final.** Comprueba el README remoto, la página de lanzamientos, los temas, la CI y los enlaces.

## Puerta de Privacidad (Privacy Gate)

Inspecciona el conjunto preparado (staged) o rastreado (tracked), no solo el árbol de trabajo visible.

```bash
git diff --cached --check
git ls-files
rg -n "C:\\\\Us[e]rs\\\\|C:/Us[e]rs/|/c/Us[e]rs/|s[k]-[A-Za-z0-9]|gh[p]_|gh[o]_|API[_-]?KEY|TO[K]EN|PASS[W]ORD|SEC[R]ET|\\x{C3}|\\x{C2}|\\x{FFFD}" .
```

Para módulos públicos, documenta también un `RELEASE_GATE.md` o puerta equivalente: fecha, comandos ejecutados, resultado, advertencias restantes y excepciones intencionadas. Si alguna vez se incluyó un secreto en un commit, eliminarlo de `HEAD` no es suficiente; rota el secreto.

## Metadatos de GitHub

Después del push, establece los metadatos y los datos de lanzamiento de forma explícita.

```bash
gh repo edit ORG/REPO --description "Descripción corta y concreta" \
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

Si la CI está en rojo después de un lanzamiento, el repositorio aún no se ha publicado de forma limpia. Para un lanzamiento inicial recién creado, mover de forma inmediata e intencionada la etiqueta recién creada al commit corregido es aceptable.

## Errores frecuentes

| Error | Solución |
|---|---|
| `.gitignore` se añade después de `git add` | Quitar del staging primero, corregir reglas de ignore y volver a añadir |
| README es monolingüe aunque la UI o skill sea multilingüe | Añadir enlaces de idioma o READMEs localizados |
| Sin banner, temas o descripción | Añadir activos de descubrimiento antes del anuncio |
| La etiqueta de lanzamiento existe, pero la CI está en rojo | Corregir la CI y verificar la nueva ejecución |
| Se actualiza el README de la organización, pero se omite `llms.txt` | Actualizar tanto las superficies legibles por humanos como por máquinas |
| Una ruta local aparece en la documentación pública | Reemplazarla con rutas relativas o ejemplos genéricos |
| El repositorio público contiene una base de datos de pruebas o bandeja de entrada de notebooks | Eliminar del rastreo, añadir reglas de ignore y volver a ejecutar la puerta de privacidad |

## Lista de comprobación final

- [ ] Reglas locales y bloqueos comprobados.
- [ ] `.gitignore` existía antes del primer add.
- [ ] Documentos públicos, licencia, seguridad, contribución, changelog y `llms.txt` presentes.
- [ ] README incluye nombre del repo, propósito, instalación, uso, privacidad y licencia.
- [ ] Expectativa de i18n cumplida.
- [ ] Banner, logo o captura de pantalla presentes cuando sea útil.
- [ ] Pruebas y verificaciones básicas (smokes) superadas.
- [ ] Escaneos de privacidad, rutas, secretos, bases de datos y mojibake limpios.
- [ ] Descripción de GitHub, temas, etiqueta, release y CI verificados.
- [ ] Perfil de organización, registro y enlaces del ecosistema actualizados.

## Historial de cambios

### 1.0.0 (2026-06-18)
- Creado el protocolo inicial de mantenimiento y publicación de repositorios.