# PR #8 — Feature/docker compose

**Responsable:** Andrés Silva (`Jandresi`)  
**Proyecto:** Gestor de Incidencias  
**Pull request:** [#8](https://github.com/kmolano-dot/gestor-incidencias/pull/8)  
**Rama:** `feature/docker-compose` → `main`  
**Integrado:** 9 de noviembre de 2026, 08:08 (hora de Colombia)

## Contexto

La aplicación ya necesitaba una base PostgreSQL para funcionar (PR #5), y cada integrante tenía que instalarla y configurarla por su cuenta. Hacía falta poder levantar todo el entorno con un solo comando.

## Qué se hizo

- `dockerfile`: imagen de la aplicación sobre `python:3.10-slim`, que instala las dependencias y ejecuta Flask en el puerto 5000.
- `docker-compose.yaml`: servicio `db` (`postgres:18-alpine`, con volumen persistente, healthcheck y carga inicial del esquema) y servicio `web`, que espera a que la base esté saludable.
- `.env.example`: variables de PostgreSQL y `DATABASE_URL` con marcadores en lugar de valores reales.

## Evidencia

Datos tomados de GitHub el 24 de noviembre de 2026.

| Dato | Valor |
| --- | --- |
| Abierto | 8 de noviembre de 2026, 20:15 |
| Integrado | 9 de noviembre de 2026, 08:08 |
| Fusionado por | Diego Fernando Gaitán Avella (`gaitandiego`) |
| Commit de fusión | [`7f7293c`](https://github.com/kmolano-dot/gestor-incidencias/commit/7f7293c8b936604937a4b350cb2afb49cc542e76) |
| Tamaño | 5 archivos, +156 −60 líneas |

### Commits

| Commit | Fecha | Autor | Mensaje |
| --- | --- | --- | --- |
| [`790cad9`](https://github.com/kmolano-dot/gestor-incidencias/commit/790cad9166af93297a85f52da3044c452bc2a438) | 8 de noviembre de 2026 | uriel_andres_rincon | feat: integrar Flask con PostgreSQL |
| [`657d8d8`](https://github.com/kmolano-dot/gestor-incidencias/commit/657d8d8bdd0ec85048c9c6f1f6c29b2556d83a8f) | 8 de noviembre de 2026 | uriel_andres_rincon | merge: integrar pruebas automatizadas de main |
| [`87bdced`](https://github.com/kmolano-dot/gestor-incidencias/commit/87bdced6a0d1cc1f430e69409e090fa84c06d47e) | 8 de noviembre de 2026 | Jandresi | Feat: Se dockeriza flask y postgresql con compose |

### Archivos

| Archivo | Líneas |
| --- | --- |
| `.env.example` | +9 −0 |
| `app.py` | +90 −59 |
| `docker-compose.yaml` | +32 −0 |
| `dockerfile` | +23 −0 |
| `requirements.txt` | +2 −1 |

### Revisión

| Revisor | Resultado | Fecha |
| --- | --- | --- |
| Diego Fernando Gaitán Avella (`gaitandiego`) | Aprobado | 9 de noviembre de 2026 |

### Checks automáticos

| Check | Resultado |
| --- | --- |
| Pytest sobre Python 3.11 | Fallido |
| Pytest sobre Python 3.12 | Fallido |

## Notas

- La rama contenía también los dos commits del PR #5, por eso `app.py` y `requirements.txt` aparecen entre los archivos. El aporte propio de este pull request es el commit `87bdced`.
- Reemplaza a los PR #6 y #7, que se cerraron sin integrar.
- Los checks terminaron en fallo por la misma causa que en el PR #5. `main` quedó con las pruebas en rojo hasta el PR #9.
