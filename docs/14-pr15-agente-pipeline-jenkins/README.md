# PR #15 — feat: crear agente y pipeline manual de Jenkins

**Responsable:** Uriel Andrés Rincón (`urielAndresRincon`)  
**Proyecto:** Gestor de Incidencias  
**Pull request:** [#15](https://github.com/kmolano-dot/gestor-incidencias/pull/15)  
**Rama:** `feature/jenkins-pipeline-grupal` → `main`  
**Integrado:** 22 de noviembre de 2026, 11:32 (hora de Colombia)

## Contexto

Con Jenkins disponible, el siguiente paso era tener un agente propio del proyecto y un primer pipeline que demostrara que el entorno funcionaba, antes de sumar pruebas o disparadores.

## Qué se hizo

- `Jenkinsfile`: pipeline declarativo que pide el agente con la etiqueta `gestor-incidencias` y ejecuta la etapa `Verificar agente`, que muestra las versiones de Python, Git y Java.
- `docs/02-integracion-jenkins/uriel/uriel-agente-pipeline.md`: procedimiento de creación, configuración y conexión del agente mediante Docker, con 14 capturas.

## Evidencia

Datos tomados de GitHub el 24 de noviembre de 2026.

| Dato | Valor |
| --- | --- |
| Abierto | 14 de noviembre de 2026, 19:12 |
| Integrado | 22 de noviembre de 2026, 11:32 |
| Fusionado por | Diego Fernando Gaitán Avella (`gaitandiego`) |
| Commit de fusión | [`cfe93d0`](https://github.com/kmolano-dot/gestor-incidencias/commit/cfe93d03503d9cf390466a15b768dce21184d39b) |
| Tamaño | 16 archivos, +173 −0 líneas |

### Commits

| Commit | Fecha | Autor | Mensaje |
| --- | --- | --- | --- |
| [`f5e3bc8`](https://github.com/kmolano-dot/gestor-incidencias/commit/f5e3bc8f2d230e7e0fbf5b5b30eecf8ba3563324) | 14 de noviembre de 2026 | uriel_andres_rincon | feat: crear agente y pipeline manual de Jenkins con evidencias |
| [`11c08de`](https://github.com/kmolano-dot/gestor-incidencias/commit/11c08deab6bf42325c58aa64ac009379bc658494) | 14 de noviembre de 2026 | uriel_andres_rincon | docs: corregir captura de configuracion del pipeline |

### Archivos

| Archivo | Líneas |
| --- | --- |
| `Jenkinsfile` | +21 −0 |
| `docs/02-integracion-jenkins/uriel/uriel-agente-pipeline.md` | +152 −0 |
| `docs/02-integracion-jenkins/uriel/` | 14 capturas PNG |

### Revisión

| Revisor | Resultado | Fecha |
| --- | --- | --- |
| Diego Fernando Gaitán Avella (`gaitandiego`) | Aprobado | 22 de noviembre de 2026 |

### Checks automáticos

| Check | Resultado |
| --- | --- |
| Pytest sobre Python 3.11 | Correcto |
| Pytest sobre Python 3.12 | Correcto |

## Notas

- Resultado declarado en el pull request: la ejecución manual #1 terminó en `Finished: SUCCESS`, con Python 3.12.16, Git 2.47.3 y Java 21.0.13.
- El pipeline se ejecutó a mano y sin disparadores. No ejecuta pruebas ni se conecta a PostgreSQL; eso llegó con el PR #16.
- El agente se montó sobre el servidor de laboratorio de Uriel, externo a `compose.jenkins.yaml`.

## Documentación relacionada

- [Documento del agente y el pipeline](../02-integracion-jenkins/uriel/uriel-agente-pipeline.md)
