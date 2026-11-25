# Respaldo técnico — conexión de agente Jenkins a PostgreSQL de pruebas

**Autor de la validación local:** Uriel Andrés Rincón.  
**Proyecto:** Gestor de Incidencias.  
**Alcance:** alternativa de respaldo para revisión del equipo; no representa una ejecución realizada por Lina.  
**Estado de la prueba histórica:** en el entorno de Uriel se verificó la conexión desde el agente `jenkins-gestor-incidencias` a PostgreSQL y la ejecución #4 del trabajo `gestor-incidencias-pipeline` terminó correctamente, con informes de pruebas sin fallos reportados. Esta evidencia corresponde al entorno local y no equivale a una comprobación automática de este archivo Compose.

## Contexto

El repositorio ya contiene `Jenkinsfile` con etapas de verificación del agente, instalación de dependencias, espera de PostgreSQL y ejecución de PyTest. También contiene `compose.pruebas.yaml`, que define un Jenkins adicional junto con PostgreSQL. El escenario de respaldo reutiliza un controlador y un agente Jenkins **ya existentes** en la red Docker `jenkins-lab-net`, sin crear otro controlador ni acceder a la base principal de desarrollo.

## Archivos incluidos en este respaldo

- `compose.agente-postgres-pruebas.yaml`: servicio opcional e independiente de PostgreSQL 16, en la red externa `jenkins-lab-net`, sin publicar puertos al exterior ni iniciar Jenkins.
- Este documento: procedimiento de instalación, comprobación y uso desde el Jenkinsfile ya integrado.

## Procedimiento reproducible

**1. Confirmar que el controlador Jenkins y el agente ya existen.**

```powershell
docker ps -a --filter "name=jenkins"
docker network inspect jenkins-lab-net --format '{{.Name}}'
```

Si el controlador está detenido, iniciar *únicamente* el controlador ya existente y verificar el nodo en **Administrar Jenkins → Nodos**. No iniciar otros laboratorios.

**2. Comprobar la existencia del contenedor de pruebas.**

```powershell
docker ps -a --filter "name=gestor_incidencias_db_pruebas"
```

Si el contenedor ya existe y corresponde a este proyecto, reutilizarlo y no ejecutar un segundo `up`. Si existe con otra configuración, revisar su origen antes de tocarlo.

**3. Para una instalación nueva, definir un secreto local sin subirlo a GitHub.**

En el archivo `.env` del directorio del repositorio (ignorado por Git) agregar una línea `POSTGRES_TEST_PASSWORD=<valor_privado>` usando una contraseña propia, sin las marcas `< >`. No copiar claves en capturas, PR ni scripts versionados. El archivo Compose no incluye ninguna contraseña predeterminada. La red `jenkins-lab-net` debe existir previamente.

**4. Arrancar solamente PostgreSQL de pruebas, si aún no existe.**

```powershell
docker compose -f compose.agente-postgres-pruebas.yaml up -d postgres-pruebas
docker ps --filter "name=gestor_incidencias_db_pruebas"
docker exec gestor_incidencias_db_pruebas pg_isready -U postgres -d gestor_incidencias_test
```

Resultado esperado de `pg_isready`: `accepting connections`. Si ya había un volumen de PostgreSQL, cambiar la variable de contraseña no cambia la clave de un usuario previamente creado: comprobar el estado antes de reutilizar datos persistidos.

**5. Verificar conectividad TCP desde el contenedor agente.**

```powershell
docker exec jenkins-gestor-incidencias python -c "import socket; s=socket.create_connection(('gestor_incidencias_db_pruebas',5432),5); print('Conexion TCP exitosa con PostgreSQL'); s.close()"
```

La conexión TCP demuestra acceso de red, no autenticación. Se usa el puerto **5432 dentro de Docker**, no el puerto que eventualmente se publique en Windows.

**6. Comprobar autenticación desde Jenkins, sin publicar secretos.**

En **Administrar Jenkins → Credenciales → System → Global**, crear una credencial `Secret text` con ID `test-database-url` y valor:

```text
postgresql://postgres:<CONTRASENA_PRIVADA>@gestor_incidencias_db_pruebas:5432/gestor_incidencias_test
```

Reemplazar el marcador por la clave local. Si la contraseña contiene caracteres reservados de una URL, codificarlos para la parte de contraseña. No incluir etiquetas como “Cadena de conexión:” en el secreto. No imprimir ni capturar ese valor. Jenkins usa esta credencial mediante `TEST_DATABASE_URL = credentials('test-database-url')` en el Jenkinsfile existente.

**7. Ejecutar el Jenkinsfile que ya existe.**

En el trabajo `gestor-incidencias-pipeline`, configurar **Pipeline script from SCM**, SCM `Git`, URL `https://github.com/kmolano-dot/gestor-incidencias.git`, rama `*/main` y ruta `Jenkinsfile`. En Jenkins seleccionar **Construir ahora** y revisar el resultado. Si se está probando esta rama antes de fusionar, ajustar temporalmente el selector a la rama del PR y después restablecerlo. El Jenkinsfile debe ejecutarse en el nodo con etiqueta `gestor-incidencias`.

**8. Revisar las etapas y evidencias.**

- Verificar agente.
- Instalar dependencias.
- Esperar base de datos: mensaje `PostgreSQL de pruebas disponible`.
- Pruebas PyTest: publicar `resultados-pruebas.xml` y `coverage.xml`.

Guardar capturas del agente conectado, del contenedor sano, de la prueba TCP y del resultado final; ocultar secretos. Confirmar el número exacto de pruebas desde el informe antes de incluirlo en un documento.

## Incidencia encontrada en la validación de Uriel

La primera ejecución del pipeline desde SCM (#3) no pasó la espera de PostgreSQL. La consola indicó que el valor de `TEST_DATABASE_URL` no era una URL de conexión válida (`falta "=" después de "Cadena"`). Se actualizó el valor de la credencial existente, sin alterar su ID ni el `Jenkinsfile`. La ejecución posterior (#4) apareció como correcta y publicó los informes. Se trata de evidencia de un entorno local, no de pruebas ejecutadas automáticamente por este PR.

## Límites y precauciones

- La base de pruebas es independiente de `gestor_incidencias_db`; las pruebas modifican objetos y datos de `gestor_incidencias_test`.
- El Compose alternativo está pensado únicamente para un agente existente en `jenkins-lab-net`; no sustituye `compose.pruebas.yaml` de otros integrantes.
- La instalación real del agente y sus secretos no son transportados por GitHub: deben existir y configurarse en cada entorno.
- Este archivo Compose no ha sido ejecutado todavía como parte del PR. Requiere revisión en Docker, especialmente la persistencia del volumen, el acceso del agente y la credencial de Jenkins.
- Antes de fusionar, comparar este respaldo con el trabajo propio de Lina para evitar duplicación o conflicto de archivos y reconocer correctamente las contribuciones.
