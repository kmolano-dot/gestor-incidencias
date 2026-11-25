# PR #12 — docs: actualizar el README con la configuración, las rutas y las prue…

**Responsable:** Kevin (`kmolano-dot`)  
**Proyecto:** Gestor de Incidencias  
**Pull request:** [#12](https://github.com/kmolano-dot/gestor-incidencias/pull/12)  
**Rama:** `codex/actualizar-readme` → `main`  
**Integrado:** 9 de noviembre de 2026, 20:11 (hora de Colombia)

## Contexto

El README seguía describiendo el proyecto como en el primer día. Desde entonces se habían integrado la aplicación, la base de datos, los contenedores y las pruebas, y quien clonara el repositorio no tenía cómo saber levantarlo.

## Qué se hizo

- `README.md`: se reescribe para explicar la configuración de `.env`, el arranque con Docker Compose, la ejecución local de Flask, las funcionalidades y rutas HTTP, el esquema de PostgreSQL y las pruebas con una base aislada.
- Se describe también el flujo de GitHub Actions y la estructura del repositorio.

## Evidencia

Datos tomados de GitHub el 24 de noviembre de 2026.

| Dato | Valor |
| --- | --- |
| Abierto | 9 de noviembre de 2026, 20:04 |
| Integrado | 9 de noviembre de 2026, 20:11 |
| Fusionado por | Kevin (`kmolano-dot`) |
| Commit de fusión | [`d59a9d3`](https://github.com/kmolano-dot/gestor-incidencias/commit/d59a9d3e6886c05bdc856953b2a9820a0ad62f29) |
| Tamaño | 1 archivos, +119 −33 líneas |

### Commits

| Commit | Fecha | Autor | Mensaje |
| --- | --- | --- | --- |
| [`573d6a2`](https://github.com/kmolano-dot/gestor-incidencias/commit/573d6a2d758233861c8f26c9d1140e920ac776dc) | 9 de noviembre de 2026 | kmolano | docs: actualizar el README con la configuración, las rutas y las prue… |

### Archivos

| Archivo | Líneas |
| --- | --- |
| `README.md` | +119 −33 |

### Revisión

| Revisor | Resultado | Fecha |
| --- | --- | --- |
| Uriel Andrés Rincón (`urielAndresRincon`) | Aprobado | 9 de noviembre de 2026 |

### Checks automáticos

| Check | Resultado |
| --- | --- |
| Pytest sobre Python 3.11 | Correcto |
| Pytest sobre Python 3.12 | Correcto |

## Notas

- Cambio solo de documentación. La descripción indica que `git diff --check` terminó sin errores y que no se ejecutó Pytest por ese motivo.
