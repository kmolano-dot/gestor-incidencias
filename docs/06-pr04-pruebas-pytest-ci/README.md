# PR #4 — Agregar pruebas automatizadas con pytest e integracion continua

**Responsable:** Diego Fernando Gaitán Avella (`gaitandiego`)  
**Proyecto:** Gestor de Incidencias  
**Pull request:** [#4](https://github.com/kmolano-dot/gestor-incidencias/pull/4)  
**Rama:** `test/operaciones-incidencias` → `main`  
**Integrado:** 8 de noviembre de 2026, 15:53 (hora de Colombia)

## Contexto

Las funcionalidades se comprobaban a mano desde el navegador, lo que obligaba a repetir el recorrido completo en cada cambio. Hacía falta dejar esas comprobaciones en código y que se ejecutaran solas.

## Qué se hizo

- `tests/`: siete archivos de pruebas, uno por operación del gestor, más `conftest.py` con las fixtures compartidas. En total 51 casos que cubren las seis rutas de la aplicación.
- `pytest.ini`: configuración para ejecutar las pruebas con un solo comando.
- `requirements.txt`: se agregan `pytest` y `pytest-cov`.
- `.github/workflows/pruebas.yml`: flujo de GitHub Actions que ejecuta las pruebas en Python 3.11 y 3.12 en cada pull request hacia `main`.

## Evidencia

Datos tomados de GitHub el 24 de noviembre de 2026.

| Dato | Valor |
| --- | --- |
| Abierto | 8 de noviembre de 2026, 12:29 |
| Integrado | 8 de noviembre de 2026, 15:53 |
| Fusionado por | Diego Fernando Gaitán Avella (`gaitandiego`) |
| Commit de fusión | [`760121b`](https://github.com/kmolano-dot/gestor-incidencias/commit/760121bf94afc0dda79ba2c752c4dc523bf10f76) |
| Tamaño | 11 archivos, +404 −1 líneas |

### Commits

| Commit | Fecha | Autor | Mensaje |
| --- | --- | --- | --- |
| [`1d52475`](https://github.com/kmolano-dot/gestor-incidencias/commit/1d524751c57d4a61755c016c2d2ef1e04fe780bf) | 8 de noviembre de 2026 | Diego Gaitan | Agregar pruebas automatizadas con pytest e integracion continua |

### Archivos

| Archivo | Líneas |
| --- | --- |
| `.github/workflows/pruebas.yml` | +45 −0 |
| `pytest.ini` | +6 −0 |
| `requirements.txt` | +2 −1 |
| `tests/conftest.py` | +42 −0 |
| `tests/test_actualizar_estado.py` | +31 −0 |
| `tests/test_crear_incidencia.py` | +78 −0 |
| `tests/test_editar_incidencia.py` | +61 −0 |
| `tests/test_eliminar_incidencia.py` | +34 −0 |
| `tests/test_listado_filtro.py` | +60 −0 |
| `tests/test_persistencia.py` | +32 −0 |
| `tests/test_salud.py` | +13 −0 |

### Revisión

| Revisor | Resultado | Fecha |
| --- | --- | --- |
| Uriel Andrés Rincón (`urielAndresRincon`) | Aprobado | 8 de noviembre de 2026 |

### Checks automáticos

| Check | Resultado |
| --- | --- |
| Pytest sobre Python 3.11 | Correcto |
| Pytest sobre Python 3.12 | Correcto |

## Notas

- Resultado declarado en el pull request: 51 pruebas correctas y 3 omitidas, con cobertura del 100% de `app.py`. Las 3 omitidas eran las de persistencia, pendientes de la base de datos.
- Es el primer pull request del repositorio con checks automáticos.

## Documentación relacionada

- [Documento de las pruebas con capturas](../01-desarrollo-anterior/diego/diego-pruebas-pytest.md)
