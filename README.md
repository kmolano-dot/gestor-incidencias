# Gestor de incidencias

Aplicación web académica para registrar y dar seguimiento a incidencias de software. Flask renderiza la interfaz en español con Jinja y CSS, y guarda las incidencias en PostgreSQL mediante Psycopg. Docker Compose levanta ambos servicios y GitHub Actions ejecuta las pruebas automatizadas.

## Funcionalidades

- Registrar incidencias con título, descripción y prioridad (`Baja`, `Media` o `Alta`). El título admite hasta 150 caracteres y cada incidencia nueva queda en estado `Pendiente`.
- Consultar todas las incidencias o filtrarlas por estado (`Pendiente`, `En proceso` o `Resuelta`).
- Editar el título, la descripción y la prioridad. El estado se actualiza desde su propio formulario.
- Eliminar una incidencia desde el listado, con confirmación en el navegador.

## Puesta en marcha con Docker Compose

Necesitas Git y Docker con el complemento Docker Compose. Si el repositorio requiere una invitación, acéptala antes de clonarlo.

```bash
git clone https://github.com/kmolano-dot/gestor-incidencias.git
cd gestor-incidencias
cp .env.example .env
```

En PowerShell, usa `Copy-Item .env.example .env` para copiar el archivo. Edita `.env` con los valores de desarrollo:

```dotenv
POSTGRES_DB=gestor_incidencias
POSTGRES_USER=postgres
POSTGRES_PASSWORD=clave_local
DB_HOST=db
DB_PORT=5432
DATABASE_URL=postgresql://postgres:clave_local@db:5432/gestor_incidencias
```

Usa `postgres` como usuario de inicialización porque el SQL asigna a ese rol la propiedad de la tabla y la función. Si cambias la contraseña de ejemplo, actualízala también en `DATABASE_URL`. Compose carga el archivo `.env`, que está excluido de Git. Flask toma la conexión completa de `DATABASE_URL`.

```bash
docker compose up --build -d
```

Abre [http://localhost:5000](http://localhost:5000). Compose publica Flask en el puerto `5000` y PostgreSQL en el `5432`. El servicio `web` usa Python 3.10 y espera a que `db` (PostgreSQL 18 Alpine) pase su comprobación de disponibilidad con `pg_isready`.

Para consultar el estado de los servicios, usa `docker compose ps`. Para ver sus registros, usa `docker compose logs -f web db`. `docker compose down` detiene los servicios y conserva los datos en el volumen `postgres_data`. PostgreSQL ejecuta el SQL de inicialización cuando crea el clúster en un volumen vacío.

### Ejecutar Flask en el equipo

Como alternativa, puedes levantar solo PostgreSQL con `docker compose up -d --wait db` y ejecutar Flask con Python 3.10 o posterior. Usa `127.0.0.1` en `DATABASE_URL` porque Flask se ejecuta fuera de la red de Compose.

En Bash o Zsh:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export DATABASE_URL='postgresql://postgres:clave_local@127.0.0.1:5432/gestor_incidencias'
python -m flask --app app run
```

En PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:DATABASE_URL = 'postgresql://postgres:clave_local@127.0.0.1:5432/gestor_incidencias'
.\.venv\Scripts\python.exe -m flask --app app run
```

## Rutas HTTP

| Método | Ruta | Comportamiento |
| --- | --- | --- |
| `GET` | `/` | Muestra el listado ordenado por ID. Acepta el parámetro `estado`. Si se omite o es inválido, muestra todas las incidencias. |
| `POST` | `/incidencias` | Crea una incidencia con `titulo`, `descripcion` y `prioridad`. |
| `POST` | `/incidencias/<id>/editar` | Actualiza `titulo`, `descripcion` y `prioridad`. |
| `POST` | `/incidencias/<id>/estado` | Actualiza el campo `estado`. |
| `POST` | `/incidencias/<id>/eliminar` | Elimina la incidencia indicada. |
| `GET` | `/salud` | Devuelve `{"estado":"ok","servicio":"Flask"}` con HTTP 200 e indica que Flask responde. La disponibilidad de PostgreSQL se comprueba por separado. |

Las rutas `POST` reciben datos de formulario y, si la operación tiene éxito, redirigen al listado. Los datos inválidos devuelven HTTP 400. Editar, cambiar el estado o eliminar una incidencia que no existe devuelve HTTP 404.

## Base de datos

El [esquema SQL](database/gestor_incidencias.sql) crea la tabla `public.incidencias` con un ID `bigint` autogenerado, título, descripción, prioridad, estado y fechas de creación y actualización. La base valida que el título y la descripción tengan contenido y que la prioridad y el estado estén entre los valores permitidos.

La tabla tiene índices para estado y prioridad. PostgreSQL asigna ambas fechas al insertar una incidencia y un disparador actualiza `fecha_actualizacion` cuando se modifica el registro.

## Pruebas automatizadas

Pytest cubre el registro, la edición, el cambio de estado, la eliminación, el listado y sus filtros, la persistencia y la ruta `/salud`. Toda la suite requiere `TEST_DATABASE_URL` con acceso a una base dedicada llamada `gestor_incidencias_test`. Pytest verifica el nombre de la base, recrea la tabla y la función al iniciar la sesión y vacía la tabla con reinicio de IDs antes y después de cada prueba que usa el cliente Flask.

Para levantar una instancia de pruebas en el puerto `5433`, ejecuta:

```bash
docker run --rm -d --name gestor-incidencias-pruebas -p 127.0.0.1:5433:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=clave_pruebas -e POSTGRES_DB=gestor_incidencias_test postgres:16
```

Comprueba que PostgreSQL esté listo con `docker exec gestor-incidencias-pruebas pg_isready -h 127.0.0.1 -U postgres -d gestor_incidencias_test`. Si ya tienes una instancia dedicada, crea allí `gestor_incidencias_test`, usa un rol con permisos para crear y eliminar los objetos de prueba y ajusta el host, el puerto y las credenciales en la URL.

Ejecuta los comandos de tu terminal desde la raíz del repositorio. Si ya tienes `.venv` con las dependencias instaladas, puedes reutilizarlo.

### Bash o Zsh

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export TEST_DATABASE_URL='postgresql://postgres:clave_pruebas@127.0.0.1:5433/gestor_incidencias_test'
python -m pytest
```

### PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:TEST_DATABASE_URL = 'postgresql://postgres:clave_pruebas@127.0.0.1:5433/gestor_incidencias_test'
.\.venv\Scripts\python.exe -m pytest
```

Para obtener los mismos informes que en CI, agrega `--cov=app --cov-report=term-missing --cov-report=xml --junitxml=resultados-pruebas.xml` al comando de Pytest. Al terminar, puedes detener el contenedor de pruebas con `docker stop gestor-incidencias-pruebas`.

### GitHub Actions

El [flujo de pruebas](.github/workflows/pruebas.yml) se ejecuta al abrir o actualizar un pull request y al hacer push a `main`. Usa PostgreSQL 16 y ejecuta la suite con Python 3.11 y 3.12. Cada versión guarda el informe de Pytest (`resultados-pruebas.xml`) y el de cobertura (`coverage.xml`) como artefactos de la ejecución.

## Estructura del repositorio

| Archivo o directorio | Contenido |
| --- | --- |
| [`app.py`](app.py) | Rutas Flask, validación de formularios y consultas a PostgreSQL. |
| [`templates/index.html`](templates/index.html) y [`static/styles.css`](static/styles.css) | Interfaz, formularios y estilos. |
| [`database/gestor_incidencias.sql`](database/gestor_incidencias.sql) | Esquema, restricciones, índices y disparador de actualización. |
| [`dockerfile`](dockerfile) y [`docker-compose.yaml`](docker-compose.yaml) | Imagen de Flask, servicios, puertos y volumen de datos. |
| [`.env.example`](.env.example) y [`.gitignore`](.gitignore) | Configuración de ejemplo y exclusiones de archivos locales. |
| [`requirements.txt`](requirements.txt) | Dependencias de Flask, Psycopg, Pytest y pytest-cov. |
| [`tests/`](tests/) y [`pytest.ini`](pytest.ini) | Casos de prueba, preparación de la base aislada y configuración de Pytest. |
| [`.github/`](.github/) y [`CONTRIBUTING.md`](CONTRIBUTING.md) | Automatización, plantilla de pull requests y guía de colaboración. |

## Equipo y responsabilidades

| Integrante | Responsabilidad |
| --- | --- |
| Uriel Andrés Rincón | Arquitectura y aplicación Flask |
| Lina Bedoya Peña | Base de datos PostgreSQL |
| Jorge Silva Álvarez | Docker y comunicación entre contenedores |
| Diego Gaitán | Pruebas automatizadas y registro de resultados |
| Kevin Andrés Molano Gamarra | Organización en GitHub, documentación y evidencias |

## Cómo colaborar

Crea una rama desde `main` para cada cambio y abre un pull request hacia `main`. Usa la [plantilla de pull requests](.github/PULL_REQUEST_TEMPLATE.md) para explicar el cambio, cómo se comprobó y qué evidencias lo acompañan. La [guía de colaboración](CONTRIBUTING.md) detalla el flujo de ramas, commits y revisiones. Cada integrante registra sus aportes con su cuenta y documenta su proceso en el documento compartido del equipo.
