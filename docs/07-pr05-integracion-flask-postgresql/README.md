# PR #5 — Integrar Flask con PostgreSQL para persistencia de incidencias.

**Responsable:** Uriel Andrés Rincón (`urielAndresRincon`)  
**Proyecto:** Gestor de Incidencias  
**Pull request:** [#5](https://github.com/kmolano-dot/gestor-incidencias/pull/5)  
**Rama:** `feature/integracion-flask-postgresql` → `main`  
**Integrado:** 9 de noviembre de 2026, 08:08 (hora de Colombia)

## Contexto

Con el esquema de la base ya disponible (PR #3), faltaba que la aplicación dejara de usar la lista en memoria y guardara las incidencias en PostgreSQL.

## Qué se hizo

- `app.py`: se reemplaza el almacenamiento en memoria por consultas SQL con `psycopg`. La conexión se toma de la variable de entorno `DATABASE_URL`.
- Todas las operaciones (crear, listar, filtrar, editar, cambiar estado y eliminar) pasan a ejecutarse contra la tabla `incidencias`.
- `requirements.txt`: se agrega `psycopg`.

## Evidencia

Datos tomados de GitHub el 24 de noviembre de 2026.

| Dato | Valor |
| --- | --- |
| Abierto | 8 de noviembre de 2026, 16:58 |
| Integrado | 9 de noviembre de 2026, 08:08 |
| Fusionado por | Sin usuario registrado (ver notas) |
| Commit de fusión | [`7f7293c`](https://github.com/kmolano-dot/gestor-incidencias/commit/7f7293c8b936604937a4b350cb2afb49cc542e76) |
| Tamaño | 2 archivos, +92 −60 líneas |

### Commits

| Commit | Fecha | Autor | Mensaje |
| --- | --- | --- | --- |
| [`790cad9`](https://github.com/kmolano-dot/gestor-incidencias/commit/790cad9166af93297a85f52da3044c452bc2a438) | 8 de noviembre de 2026 | uriel_andres_rincon | feat: integrar Flask con PostgreSQL |
| [`657d8d8`](https://github.com/kmolano-dot/gestor-incidencias/commit/657d8d8bdd0ec85048c9c6f1f6c29b2556d83a8f) | 8 de noviembre de 2026 | uriel_andres_rincon | merge: integrar pruebas automatizadas de main |

### Archivos

| Archivo | Líneas |
| --- | --- |
| `app.py` | +90 −59 |
| `requirements.txt` | +2 −1 |

### Revisión

No hay revisiones registradas en GitHub.

### Checks automáticos

| Check | Resultado |
| --- | --- |
| Pytest sobre Python 3.11 | Fallido |
| Pytest sobre Python 3.12 | Fallido |

## Notas

- GitHub registra este pull request como integrado sin un usuario que lo fusionara: sus dos commits entraron a `main` dentro del PR #8, cuya rama los contenía. Ambos comparten el commit de fusión `7f7293c`.
- El pull request estaba marcado como borrador y no tiene revisiones registradas.
- Los checks terminaron en fallo: las pruebas del PR #4 seguían usando la lista en memoria que este cambio eliminó. Lo corrigió el PR #9.
- La descripción indica que las operaciones se verificaron a mano contra PostgreSQL, incluida la persistencia tras reiniciar Flask.
