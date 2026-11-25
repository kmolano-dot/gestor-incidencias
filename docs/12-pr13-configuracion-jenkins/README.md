# PR #13 — Add jenkins configuration

**Responsable:** Andrés Silva (`Jandresi`)  
**Proyecto:** Gestor de Incidencias  
**Pull request:** [#13](https://github.com/kmolano-dot/gestor-incidencias/pull/13)  
**Rama:** `feature/docker-compose` → `main`  
**Integrado:** 22 de noviembre de 2026, 11:31 (hora de Colombia)

## Contexto

Segunda entrega: integración continua con Jenkins. Hacía falta un servidor Jenkins que cualquier integrante pudiera levantar igual, sin pasar por el asistente de instalación ni configurar plugins a mano.

## Qué se hizo

- `compose.jenkins.yaml`: servicio `jenkins` con los puertos 8080 y 50000, el volumen `jenkins_home` y el socket de Docker del equipo montado en el contenedor.
- `jenkins/Dockerfile`: parte de `jenkins/jenkins:lts`, instala el cliente de Docker, desactiva el asistente inicial y preinstala los plugins `git`, `github`, `workflow-aggregator`, `docker-workflow` y `docker-plugin`.
- `jenkins/security.groovy`: script de inicio que crea el usuario administrador y exige iniciar sesión.

## Evidencia

Datos tomados de GitHub el 24 de noviembre de 2026.

| Dato | Valor |
| --- | --- |
| Abierto | 14 de noviembre de 2026, 13:14 |
| Integrado | 22 de noviembre de 2026, 11:31 |
| Fusionado por | Diego Fernando Gaitán Avella (`gaitandiego`) |
| Commit de fusión | [`aac8f0c`](https://github.com/kmolano-dot/gestor-incidencias/commit/aac8f0c048b6063bf29f7469b378a8ad43656338) |
| Tamaño | 3 archivos, +56 −0 líneas |

### Commits

| Commit | Fecha | Autor | Mensaje |
| --- | --- | --- | --- |
| [`367bc2a`](https://github.com/kmolano-dot/gestor-incidencias/commit/367bc2a9bbba6f2d850e75fd887a04bc639d2e5d) | 14 de noviembre de 2026 | Jandresi | Add jenkins configuration |

### Archivos

| Archivo | Líneas |
| --- | --- |
| `compose.jenkins.yaml` | +17 −0 |
| `jenkins/Dockerfile` | +27 −0 |
| `jenkins/security.groovy` | +12 −0 |

### Revisión

| Revisor | Resultado | Fecha |
| --- | --- | --- |
| Uriel Andrés Rincón (`urielAndresRincon`) | Aprobado | 14 de noviembre de 2026 |
| Diego Fernando Gaitán Avella (`gaitandiego`) | Aprobado | 22 de noviembre de 2026 |

### Checks automáticos

| Check | Resultado |
| --- | --- |
| Pytest sobre Python 3.11 | Correcto |
| Pytest sobre Python 3.12 | Correcto |

## Notas

- El usuario y la contraseña del administrador quedaron escritos en `jenkins/security.groovy`. El PR #17 los trasladó al archivo `.env`.
- El contenedor se ejecuta como `root` y monta `/var/run/docker.sock`, de modo que Jenkins puede controlar el Docker del equipo anfitrión.
- La descripción del pull request se completó de forma retroactiva el 24 de noviembre de 2026 a partir del diff.
