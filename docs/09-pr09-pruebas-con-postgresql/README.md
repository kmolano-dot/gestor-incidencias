# PR #9 — Adaptar las pruebas automatizadas a PostgreSQL y agregar el servicio…

**Responsable:** Diego Fernando Gaitán Avella (`gaitandiego`)  
**Proyecto:** Gestor de Incidencias  
**Pull request:** [#9](https://github.com/kmolano-dot/gestor-incidencias/pull/9)  
**Rama:** `test/pruebas-con-postgresql` → `main`  
**Integrado:** 9 de noviembre de 2026, 19:53 (hora de Colombia)

## Contexto

Al integrarse los PR #5 y #8, las pruebas automatizadas quedaron en rojo en `main`: la preparación de datos reiniciaba una lista en memoria que `app.py` ya no usaba. El error era `AttributeError: module 'app' has no attribute 'incidencias'`.

## Qué se hizo

- `tests/conftest.py`: se conecta a PostgreSQL, carga el esquema desde `database/gestor_incidencias.sql` y limpia la tabla con `TRUNCATE ... RESTART IDENTITY` entre pruebas.
- `tests/test_persistencia.py`: las tres pruebas que estaban omitidas se activan y pasan a ser cinco.
- `.github/workflows/pruebas.yml`: se agrega un servicio PostgreSQL 16 y el flujo pasa a ejecutarse en cualquier pull request.
- `pytest.ini`: se retira el marcador `postgres`, que ya no hacía falta.

## Evidencia

Datos tomados de GitHub el 24 de noviembre de 2026.

| Dato | Valor |
| --- | --- |
| Abierto | 9 de noviembre de 2026, 08:35 |
| Integrado | 9 de noviembre de 2026, 19:53 |
| Fusionado por | Kevin (`kmolano-dot`) |
| Commit de fusión | [`fd36d1f`](https://github.com/kmolano-dot/gestor-incidencias/commit/fd36d1f24885ffcb9f77558a805bdb18c69771e4) |
| Tamaño | 4 archivos, +124 −23 líneas |

### Commits

| Commit | Fecha | Autor | Mensaje |
| --- | --- | --- | --- |
| [`1830fed`](https://github.com/kmolano-dot/gestor-incidencias/commit/1830fed3551c0cfbc1541628724e966ef5c8e34d) | 9 de noviembre de 2026 | Diego Gaitan | Adaptar las pruebas automatizadas a PostgreSQL y agregar el servicio … |
| [`26bf3f7`](https://github.com/kmolano-dot/gestor-incidencias/commit/26bf3f782429100f82566c3b25f931a4082e8c93) | 9 de noviembre de 2026 | Diego Gaitan | Adaptar las pruebas automatizadas a PostgreSQL y agregar el servicio … |

### Archivos

| Archivo | Líneas |
| --- | --- |
| `.github/workflows/pruebas.yml` | +18 −1 |
| `pytest.ini` | +0 −2 |
| `tests/conftest.py` | +76 −8 |
| `tests/test_persistencia.py` | +30 −12 |

### Revisión

| Revisor | Resultado | Fecha |
| --- | --- | --- |
| Kevin (`kmolano-dot`) | Aprobado | 9 de noviembre de 2026 |
| Uriel Andrés Rincón (`urielAndresRincon`) | Aprobado | 9 de noviembre de 2026 |

### Checks automáticos

| Check | Resultado |
| --- | --- |
| Pytest sobre Python 3.11 | Correcto |
| Pytest sobre Python 3.12 | Correcto |

## Notas

- Resultado declarado en el pull request: 56 pruebas correctas y cobertura del 100% de `app.py`.
- Los seis archivos de pruebas por ruta no se tocaron: las aserciones pasan por un ayudante de `conftest.py`.
- La rama recibió además el PR #10, que se fusionó sobre ella antes de integrarse a `main`.
- El pull request señaló dos pendientes para el equipo: acordar un `.gitattributes` por los cambios de fin de línea y exigir los checks antes de fusionar.

## Documentación relacionada

- [Documento de las pruebas con capturas](../01-desarrollo-anterior/diego/diego-pruebas-pytest.md)
