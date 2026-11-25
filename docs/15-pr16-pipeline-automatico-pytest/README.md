# PR #16 — feat: ejecucion automatica del pipeline con pruebas Pytest

**Responsable:** Diego Fernando Gaitán Avella (`gaitandiego`)  
**Proyecto:** Gestor de Incidencias  
**Pull request:** [#16](https://github.com/kmolano-dot/gestor-incidencias/pull/16)  
**Rama:** `test/pipeline-pytest` → `main`  
**Integrado:** 24 de noviembre de 2026, 18:30 (hora de Colombia)

## Contexto

El pipeline solo verificaba el agente y había que lanzarlo a mano. Faltaba que arrancara solo ante cambios en el repositorio y que ejecutara las pruebas Pytest que ya existían.

## Qué se hizo

- `Jenkinsfile`: se conserva la etapa de verificación y se agregan `Instalar dependencias`, `Esperar base de datos` y `Pruebas Pytest`. Se añade el disparador `pollSCM`, la credencial `test-database-url` y la publicación del informe JUnit y de cobertura.
- `compose.pruebas.yaml`: servidor Jenkins y una base PostgreSQL exclusiva para las pruebas.
- `jenkins/Dockerfile`: se agregan Python, `libpq-dev` y los plugins `junit`, `credentials-binding` y `timestamper`.
- Documentación de las pruebas de la primera entrega (7 capturas) y de la ejecución automática (10 capturas).

## Evidencia

Datos tomados de GitHub el 24 de noviembre de 2026.

| Dato | Valor |
| --- | --- |
| Abierto | 22 de noviembre de 2026, 12:27 |
| Integrado | 24 de noviembre de 2026, 18:30 |
| Fusionado por | Diego Fernando Gaitán Avella (`gaitandiego`) |
| Commit de fusión | [`8d6a5f3`](https://github.com/kmolano-dot/gestor-incidencias/commit/8d6a5f3bab7b05fca11bb91b2866edd11af19812) |
| Tamaño | 24 archivos, +685 −243 líneas |

### Commits

| Commit | Fecha | Autor | Mensaje |
| --- | --- | --- | --- |
| [`c512d58`](https://github.com/kmolano-dot/gestor-incidencias/commit/c512d585fb0ab8eb23917a10c60a80833f924272) | 22 de noviembre de 2026 | Diego Gaitan | feat: ejecutar las pruebas Pytest automaticamente desde Jenkins |
| [`0c4baf8`](https://github.com/kmolano-dot/gestor-incidencias/commit/0c4baf8d940f5984525e15477c75316429e81331) | 22 de noviembre de 2026 | Diego Gaitan | docs: agregar evidencias del nodo etiquetado y la credencial de pruebas |
| [`9d92bb3`](https://github.com/kmolano-dot/gestor-incidencias/commit/9d92bb3ea33e6bb076123b25c1044d934dc2bd98) | 22 de noviembre de 2026 | Diego Gaitan | docs: reemplazar evidencias sin el puntero del raton |
| [`8bf62be`](https://github.com/kmolano-dot/gestor-incidencias/commit/8bf62bec4ba93443d167d513c93ff4f3eac739c1) | 22 de noviembre de 2026 | Diego Gaitan | docs: recortar el puntero del raton en las evidencias |
| [`fdd7cef`](https://github.com/kmolano-dot/gestor-incidencias/commit/fdd7cefc34fcda3473012cafba3f91d9e044433c) | 22 de noviembre de 2026 | Diego Gaitan | test: comprobar el disparador automatico del pipeline |
| [`f291d2f`](https://github.com/kmolano-dot/gestor-incidencias/commit/f291d2fff5afff89fac0e5343863498a5c32d3d4) | 22 de noviembre de 2026 | Diego Gaitan | docs: documentar la ejecucion automatica del pipeline con sus evidencias |
| [`7e03334`](https://github.com/kmolano-dot/gestor-incidencias/commit/7e03334b647cf8101cc49aeaefdd71e2e002fc6b) | 22 de noviembre de 2026 | Diego Gaitan | docs: agregar evidencias de la rama, GitHub Actions y los pull requests |
| [`eb82027`](https://github.com/kmolano-dot/gestor-incidencias/commit/eb8202790147eddb775287db82fb7612c69b9d11) | 22 de noviembre de 2026 | Diego Gaitan | feat: exponer el puerto de la base de pruebas para ejecuciones locales |
| [`158a822`](https://github.com/kmolano-dot/gestor-incidencias/commit/158a82269a7b48dd68225a18515590afba902f15) | 22 de noviembre de 2026 | Diego Gaitan | docs: agregar evidencias de la ejecucion local y de la validacion de … |
| [`31e7ba0`](https://github.com/kmolano-dot/gestor-incidencias/commit/31e7ba013ec9532c02d2d52a221e0d03e280bbbb) | 22 de noviembre de 2026 | Diego Gaitan | docs: explicar por que la validacion de la base produce errores y no … |
| [`1b8cac7`](https://github.com/kmolano-dot/gestor-incidencias/commit/1b8cac7e6c29a6f995d6d7bb589d72aeaa54c67a) | 22 de noviembre de 2026 | Diego Gaitan | docs: completar las evidencias del desarrollo anterior |
| [`57df893`](https://github.com/kmolano-dot/gestor-incidencias/commit/57df893e03763b74c4d408669b8c8da29b3b5e68) | 22 de noviembre de 2026 | Diego Gaitan | docs: redactar las explicaciones de forma mas natural |
| [`6c806e0`](https://github.com/kmolano-dot/gestor-incidencias/commit/6c806e09eb25b920c6ca4afdb39c57f1d330d00f) | 23 de noviembre de 2026 | Diego Gaitan | refactor: reutilizar el Dockerfile de Jenkins existente en lugar de d… |

### Archivos

| Archivo | Líneas |
| --- | --- |
| `Jenkinsfile` | +79 −1 |
| `compose.pruebas.yaml` | +40 −0 |
| `docs/01-desarrollo-anterior/diego/diego-pruebas-pytest.md` | +164 −0 |
| `docs/01-desarrollo-anterior/uriel/uriel-aplicacion-flask.md` | +87 −87 |
| `docs/02-integracion-jenkins/diego/diego-ejecucion-automatica.md` | +144 −0 |
| `docs/02-integracion-jenkins/uriel/uriel-agente-pipeline.md` | +152 −152 |
| `jenkins/Dockerfile` | +19 −3 |
| `docs/01-desarrollo-anterior/diego/` | 7 capturas PNG |
| `docs/02-integracion-jenkins/diego/` | 10 capturas PNG |

### Revisión

| Revisor | Resultado | Fecha |
| --- | --- | --- |
| Kevin (`kmolano-dot`) | Aprobado | 24 de noviembre de 2026 |

### Checks automáticos

| Check | Resultado |
| --- | --- |
| Pytest sobre Python 3.11 | Correcto |
| Pytest sobre Python 3.12 | Correcto |

## Notas

- Resultado declarado en el pull request: ejecución #2 disparada automáticamente, 56 pruebas, 0 fallos, 20 segundos.
- El disparador es por consulta periódica y no por webhook, porque el servidor corre en `localhost`.
- El `Jenkinsfile` consulta el repositorio con `H/5 * * * *`, mientras que la documentación y la descripción del pull request indican `H/2 * * * *`.
- Los documentos de Uriel aparecen como reescritos completos (87 y 152 líneas) por un cambio de fin de línea de LF a CRLF; su contenido no cambió.
- Dejó como pendiente definir cuál de los tres montajes de Jenkins queda como oficial.

## Documentación relacionada

- [Documento de la ejecución automática](../02-integracion-jenkins/diego/diego-ejecucion-automatica.md)
- [Documento de las pruebas de la primera entrega](../01-desarrollo-anterior/diego/diego-pruebas-pytest.md)
