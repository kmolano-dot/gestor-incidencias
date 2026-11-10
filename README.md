# Gestor de incidencias

Proyecto académico para gestionar incidencias de software y practicar el trabajo colaborativo con Git y GitHub. La aplicación está prevista con Python y Flask, almacenamiento en PostgreSQL y ejecución mediante Docker.

## Equipo y responsabilidades

| Integrante | Responsabilidad |
| --- | --- |
| Uriel Andrés Rincón | Arquitectura y aplicación Flask |
| Lina Bedoya Peña | Base de datos PostgreSQL |
| Jorge Silva Álvarez | Docker y comunicación entre contenedores |
| Diego Gaitán | Pruebas automatizadas y registro de resultados |
| Kevin Andrés Molano Gamarra | Organización en GitHub, documentación y evidencias |

## Tecnologías previstas

- Python y Flask para la aplicación web.
- PostgreSQL para almacenar las incidencias.
- Docker y Docker Compose para los contenedores y su comunicación.
- Pytest para las pruebas automatizadas.

## Primeros pasos

Acepta la invitación al repositorio y clónalo en tu equipo:

```bash
git clone https://github.com/kmolano-dot/gestor-incidencias.git
cd gestor-incidencias
```

Las instrucciones para ejecutar la aplicación se agregarán cuando el equipo complete la integración.

## Ejecutar las pruebas con PostgreSQL

Usa una instancia de PostgreSQL dedicada a pruebas y crea una base vacía llamada `gestor_incidencias_test`. El usuario de conexión debe poder crear tablas y funciones en esa base. En este ejemplo, la instancia escucha en el puerto `5433`.

```sh
createdb -h 127.0.0.1 -p 5433 -U USUARIO gestor_incidencias_test
```

Reemplaza `USUARIO` y `CONTRASENA` por las credenciales de esa instancia y ajusta el puerto si es necesario. Pytest recrea el esquema y vacía la tabla de incidencias durante la ejecución.

### Bash

```bash
python3 -m pip install -r requirements.txt
export TEST_DATABASE_URL='postgresql://USUARIO:CONTRASENA@127.0.0.1:5433/gestor_incidencias_test'
python3 -m pytest
```

### PowerShell

```powershell
python -m pip install -r requirements.txt
$env:TEST_DATABASE_URL = 'postgresql://USUARIO:CONTRASENA@127.0.0.1:5433/gestor_incidencias_test'
python -m pytest
```

## Cómo colaborar

Consulta la [guía de colaboración](CONTRIBUTING.md) para conocer el flujo propuesto de ramas, commits y pull requests, junto con ejemplos de nombres de ramas. Los nombres son orientativos y pueden variar según el cambio.

Cada integrante debe registrar sus aportes con su cuenta y documentar su proceso y las evidencias en el documento compartido del equipo.
