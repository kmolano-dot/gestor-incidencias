# PR #17 — Jenkins - Lectura de user y pass con .env

**Responsable:** Andrés Silva (`Jandresi`)  
**Proyecto:** Gestor de Incidencias  
**Pull request:** [#17](https://github.com/kmolano-dot/gestor-incidencias/pull/17)  
**Rama:** `feature/docker-compose` → `main`  
**Integrado:** 24 de noviembre de 2026, 18:50 (hora de Colombia)

## Contexto

El usuario y la contraseña del administrador de Jenkins estaban escritos en `jenkins/security.groovy` (PR #13), dentro del repositorio. Además, Jenkins todavía no leía el `Jenkinsfile` desde GitHub.

## Qué se hizo

- `jenkins/security.groovy`: lee `JENKINS_ADMIN_USER` y `JENKINS_ADMIN_PASSWORD` del entorno y detiene el script si falta alguna.
- `jenkins/jobs.groovy`: crea al arrancar el job `gestor-incidencias-pipeline`, que lee el `Jenkinsfile` desde GitHub, y el job `verificar-acceso-github`, que clona el repositorio y muestra el commit descargado.
- `compose.jenkins.yaml`, `jenkins/Dockerfile` y `.env.example`: se pasan las variables al contenedor, se copian todos los scripts `*.groovy` y se documentan las variables nuevas.
- `docs/02-integracion-jenkins/acceso-github-jenkins.md`: puesta en marcha, comprobación del acceso y solución de problemas.

## Evidencia

Datos tomados de GitHub el 24 de noviembre de 2026.

| Dato | Valor |
| --- | --- |
| Abierto | 22 de noviembre de 2026, 19:23 |
| Integrado | 24 de noviembre de 2026, 18:50 |
| Fusionado por | Kevin (`kmolano-dot`) |
| Commit de fusión | [`a632540`](https://github.com/kmolano-dot/gestor-incidencias/commit/a632540e210a3303cfe1d688b809fea5be41949d) |
| Tamaño | 6 archivos, +273 −4 líneas |

### Commits

| Commit | Fecha | Autor | Mensaje |
| --- | --- | --- | --- |
| [`c4f5c1c`](https://github.com/kmolano-dot/gestor-incidencias/commit/c4f5c1c9b650ed8a50b2c4793c4518b9f232dbf4) | 22 de noviembre de 2026 | Jandresi | Jenkins - Lectura de user y pass con .env |
| [`87495f3`](https://github.com/kmolano-dot/gestor-incidencias/commit/87495f3c8846bcb3b88a5eddb266309f8b52c922) | 23 de noviembre de 2026 | Jandresi | Jenkins tiene acceso al repo de github |
| [`f68c3b5`](https://github.com/kmolano-dot/gestor-incidencias/commit/f68c3b5e29a0119218855f09cbf4d197297855fb) | 24 de noviembre de 2026 | kmolano | Merge branch 'main' into feature/docker-compose |

### Archivos

| Archivo | Líneas |
| --- | --- |
| `.env.example` | +11 −1 |
| `compose.jenkins.yaml` | +7 −0 |
| `docs/02-integracion-jenkins/acceso-github-jenkins.md` | +122 −0 |
| `jenkins/Dockerfile` | +2 −2 |
| `jenkins/jobs.groovy` | +123 −0 |
| `jenkins/security.groovy` | +8 −1 |

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

- El commit `f68c3b5` es una fusión de `main` en la rama para resolver un conflicto en `jenkins/Dockerfile` con el PR #16. Se conservaron Python y los plugins de `main` junto con la copia de `*.groovy` de esta rama.
- El job `gestor-incidencias-pipeline` queda en cola en este Jenkins porque el `Jenkinsfile` pide un agente con la etiqueta `gestor-incidencias`, que aquí no existe.
- La contraseña anterior sigue visible en el historial de Git.
- Tras integrarse, `compose.pruebas.yaml` quedó sin pasar las variables del administrador. El PR #18, todavía abierto al escribir este documento, lo corrige.
- La descripción del pull request se completó de forma retroactiva el 24 de noviembre de 2026 a partir del diff.

## Documentación relacionada

- [Documento del acceso a GitHub desde Jenkins](../02-integracion-jenkins/acceso-github-jenkins.md)
