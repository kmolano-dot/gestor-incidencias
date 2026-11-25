# PR #10 — fix(tests): aislar la base de datos de pytest

**Responsable:** Kevin (`kmolano-dot`)  
**Proyecto:** Gestor de Incidencias  
**Pull request:** [#10](https://github.com/kmolano-dot/gestor-incidencias/pull/10)  
**Rama:** `codex/aislar-postgresql-pruebas` → `test/pruebas-con-postgresql`  
**Integrado:** 9 de noviembre de 2026, 19:53 (hora de Colombia)

## Contexto

Las pruebas usaban `DATABASE_URL`, la misma variable que usa Flask. Si esa variable apuntaba a la base de la aplicación, Pytest podía ejecutar `DROP` y `TRUNCATE` sobre los datos reales del equipo.

## Qué se hizo

- `tests/conftest.py`: Pytest exige la variable `TEST_DATABASE_URL`, comprueba que apunte a `gestor_incidencias_test` y, ya conectado, confirma con PostgreSQL en qué base está antes de modificar nada.
- Flask usa la URL validada durante la sesión de pruebas y recupera su configuración al terminar. Los mensajes de error omiten la URL y las credenciales.
- `.github/workflows/pruebas.yml`: se configura la variable nueva.
- `README.md`: instrucciones para ejecutar las pruebas desde Bash y PowerShell.

## Evidencia

Datos tomados de GitHub el 24 de noviembre de 2026.

| Dato | Valor |
| --- | --- |
| Abierto | 9 de noviembre de 2026, 19:44 |
| Integrado | 9 de noviembre de 2026, 19:53 |
| Fusionado por | Kevin (`kmolano-dot`) |
| Commit de fusión | [`ea474d7`](https://github.com/kmolano-dot/gestor-incidencias/commit/ea474d719f916e8893a188a373522cf3efa4418e) |
| Tamaño | 3 archivos, +80 −23 líneas |

### Commits

| Commit | Fecha | Autor | Mensaje |
| --- | --- | --- | --- |
| [`ccf144f`](https://github.com/kmolano-dot/gestor-incidencias/commit/ccf144fd0e84e90f660048ee49aa182f0f91d98a) | 9 de noviembre de 2026 | kmolano | fix(tests): aislar la base de datos de pytest |

### Archivos

| Archivo | Líneas |
| --- | --- |
| `.github/workflows/pruebas.yml` | +2 −3 |
| `README.md` | +27 −1 |
| `tests/conftest.py` | +51 −19 |

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

- Este pull request no apuntaba a `main` sino a `test/pruebas-con-postgresql`, la rama del PR #9. Llegó a `main` cuando se integró el PR #9.
- La descripción indica que la suite completa quedó pendiente de ejecución en GitHub Actions; los checks registrados terminaron correctamente.

## Documentación relacionada

- [Explicación de la validación de la base (paso 6)](../01-desarrollo-anterior/diego/diego-pruebas-pytest.md)
