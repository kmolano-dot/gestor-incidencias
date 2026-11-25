# PR #2 — incorporar aplicación Flask para gestionar incidencias

**Responsable:** Uriel Andrés Rincón (`urielAndresRincon`)  
**Proyecto:** Gestor de Incidencias  
**Pull request:** [#2](https://github.com/kmolano-dot/gestor-incidencias/pull/2)  
**Rama:** `feature/registro-consulta-incidencias` → `main`  
**Integrado:** 7 de noviembre de 2026, 17:55 (hora de Colombia)

## Contexto

Primera versión funcional del Gestor de Incidencias. Hasta este punto el repositorio solo tenía documentación. Se necesitaba una aplicación web con la que registrar y administrar incidencias de software, aunque todavía sin base de datos.

## Qué se hizo

- `app.py`: aplicación Flask con las rutas para listar y filtrar incidencias, crearlas, editarlas, cambiar su estado, eliminarlas y comprobar la salud del servicio.
- `templates/index.html` y `static/styles.css`: interfaz web con el formulario de registro, el listado y las acciones sobre cada incidencia.
- `requirements.txt`: dependencia de Flask.
- Las incidencias se guardan en una lista en memoria. El segundo commit agrega la validación de la longitud máxima del título.

## Evidencia

Datos tomados de GitHub el 24 de noviembre de 2026.

| Dato | Valor |
| --- | --- |
| Abierto | 7 de noviembre de 2026, 11:12 |
| Integrado | 7 de noviembre de 2026, 17:55 |
| Fusionado por | Kevin (`kmolano-dot`) |
| Commit de fusión | [`0bf47ab`](https://github.com/kmolano-dot/gestor-incidencias/commit/0bf47ab430b8d0f0847227420d38db7b2f7ccc0d) |
| Tamaño | 4 archivos, +784 −0 líneas |

### Commits

| Commit | Fecha | Autor | Mensaje |
| --- | --- | --- | --- |
| [`89f4eed`](https://github.com/kmolano-dot/gestor-incidencias/commit/89f4eed665a910aef8286fb73a77d9111353f676) | 7 de noviembre de 2026 | uriel_andres_rincon | Agregar aplicacion Flask para gestionar incidencias |
| [`ee61045`](https://github.com/kmolano-dot/gestor-incidencias/commit/ee6104548a0ebb7dc982db99c4a2640379b0e27c) | 7 de noviembre de 2026 | uriel_andres_rincon | Validar longitud maxima del titulo en Flask |

### Archivos

| Archivo | Líneas |
| --- | --- |
| `app.py` | +111 −0 |
| `requirements.txt` | +2 −0 |
| `static/styles.css` | +509 −0 |
| `templates/index.html` | +162 −0 |

### Revisión

| Revisor | Resultado | Fecha |
| --- | --- | --- |
| Kevin (`kmolano-dot`) | Aprobado | 7 de noviembre de 2026 |

### Checks automáticos

No hay checks registrados en este pull request.

## Notas

- Las funcionalidades se comprobaron a mano en el entorno local, según la descripción del pull request.
- No hay checks registrados: el flujo de GitHub Actions llegó con el PR #4.

## Documentación relacionada

- [Documento de desarrollo con capturas](../01-desarrollo-anterior/uriel/uriel-aplicacion-flask.md)
