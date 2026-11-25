# PR #3 — Agregar esquema PostgreSQL de incidencias

**Responsable:** Lina (`LinaMarcela8`)  
**Proyecto:** Gestor de Incidencias  
**Pull request:** [#3](https://github.com/kmolano-dot/gestor-incidencias/pull/3)  
**Rama:** `feature/modelo-datos-postgresql` → `main`  
**Integrado:** 8 de noviembre de 2026, 11:30 (hora de Colombia)

## Contexto

La aplicación guardaba las incidencias en memoria y las perdía al reiniciarse. Para darle persistencia hacía falta definir primero la estructura de la base de datos PostgreSQL.

## Qué se hizo

- `database/gestor_incidencias.sql`: esquema de la base con la tabla `incidencias` y sus siete columnas, la clave primaria, la secuencia del identificador, las restricciones de validación y los índices por estado y prioridad.
- Una función con su trigger que actualiza automáticamente la fecha de modificación.

## Evidencia

Datos tomados de GitHub el 24 de noviembre de 2026.

| Dato | Valor |
| --- | --- |
| Abierto | 8 de noviembre de 2026, 00:26 |
| Integrado | 8 de noviembre de 2026, 11:30 |
| Fusionado por | Diego Fernando Gaitán Avella (`gaitandiego`) |
| Commit de fusión | [`00d6a6e`](https://github.com/kmolano-dot/gestor-incidencias/commit/00d6a6e667d54c89f3b4f8801b829ad9e45e1e7a) |
| Tamaño | 1 archivos, +130 −0 líneas |

### Commits

| Commit | Fecha | Autor | Mensaje |
| --- | --- | --- | --- |
| [`b8d3d5f`](https://github.com/kmolano-dot/gestor-incidencias/commit/b8d3d5f1aba5db26cf1492a91a4bc5ca715b3244) | 7 de noviembre de 2026 | LinaMarcela8 | Agregar esquema PostgreSQL de incidencias |

### Archivos

| Archivo | Líneas |
| --- | --- |
| `database/gestor_incidencias.sql` | +130 −0 |

### Revisión

| Revisor | Resultado | Fecha |
| --- | --- | --- |
| Diego Fernando Gaitán Avella (`gaitandiego`) | Aprobado | 8 de noviembre de 2026 |

### Checks automáticos

No hay checks registrados en este pull request.

## Notas

- La descripción del pull request incluye cinco capturas de pgAdmin (columnas, estructura, registros, restricciones y trigger) alojadas en GitHub.
- El archivo es un volcado generado por PostgreSQL 18. El PR #9 tuvo que descartar algunos ajustes de sesión para cargarlo en otras versiones.
- La conexión con Flask quedó fuera de este cambio; se hizo en el PR #5.
- No hay checks registrados: el flujo de GitHub Actions llegó con el PR #4.
