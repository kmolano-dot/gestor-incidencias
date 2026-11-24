# Configuración del acceso a GitHub desde Jenkins

**Proyecto:** Gestor de Incidencias  
**Alcance:** configurar un job de Jenkins que lea el `Jenkinsfile` desde GitHub y comprobar el acceso al repositorio sin exponer credenciales.

## 1. Qué se configuró

El Jenkins definido en `compose.jenkins.yaml` ahora crea automáticamente dos jobs al arrancar:

| Job | Tipo | Función |
| --- | --- | --- |
| `gestor-incidencias-pipeline` | Pipeline script from SCM | Lee el `Jenkinsfile` directamente desde GitHub. |
| `verificar-acceso-github` | Freestyle con Git SCM | Clona el repositorio en el nodo integrado y muestra el commit descargado. |

> Estos jobs se crean en el Jenkins definido en este repositorio. El servidor de laboratorio que usó Uriel es externo a este `compose.jenkins.yaml`, por lo que no ejecuta estos scripts ni lee este `.env`.

La configuración se toma de `.env`, que está excluido de Git:

```dotenv
GITHUB_REPO_URL=https://github.com/kmolano-dot/gestor-incidencias.git
GITHUB_BRANCH=main
GITHUB_USER=
GITHUB_TOKEN=
```

Como el repositorio es público, `GITHUB_TOKEN` puede quedar vacío: Jenkins clona de forma anónima y no hay ninguna credencial que ocultar. Si el repositorio se vuelve privado, basta con llenar `GITHUB_USER` y `GITHUB_TOKEN`; el script crea en Jenkins la credencial `github-credentials` sin escribir el token en el repositorio.

## 2. Archivos modificados

| Archivo | Cambio |
| --- | --- |
| `jenkins/jobs.groovy` | Script de inicialización que crea/actualiza los dos jobs. |
| `jenkins/Dockerfile` | Copia todos los scripts `*.groovy` a `init.groovy.d`. |
| `compose.jenkins.yaml` | Pasa a Jenkins solo las variables de Jenkins y GitHub. |
| `.env.example` | Documenta las variables nuevas. |

## 3. Puesta en marcha

> **Requisito:** Docker Desktop debe estar iniciado.

Si ya existía el volumen `jenkins_home`, los scripts nuevos no se copian automáticamente porque la imagen solo copia los archivos que faltan. Para esta práctica se recomienda empezar con un volumen limpio:

```powershell
docker compose -f compose.jenkins.yaml down -v
docker compose -f compose.jenkins.yaml up -d --build
```

> `down -v` elimina la configuración guardada de Jenkins. No borra el repositorio ni el archivo `.env`. El usuario admin se vuelve a crear desde `.env`.

Si prefieres conservar el volumen, elimina solo los scripts viejos y reinicia:

```powershell
docker compose -f compose.jenkins.yaml exec -u root jenkins rm -f /var/jenkins_home/init.groovy.d/security.groovy /var/jenkins_home/init.groovy.d/jobs.groovy
docker compose -f compose.jenkins.yaml restart jenkins
```

Espera a que Jenkins termine de arrancar:

```powershell
docker compose -f compose.jenkins.yaml logs -f jenkins
```

Abre `http://localhost:8080` e inicia sesión con `JENKINS_ADMIN_USER` y `JENKINS_ADMIN_PASSWORD`.

## 4. Comprobar el acceso al repositorio

1. En Jenkins, abre el job **verificar-acceso-github**.
2. Pulsa **Construir ahora**.
3. Abre **Console Output**.

La consola debe mostrar algo similar a:

```text
Cloning repository https://github.com/kmolano-dot/gestor-incidencias.git
...
Commit descargado:
  Hash:    <hash del commit>
  Autor:   <autor>
  Mensaje: <mensaje del commit>
Acceso al repositorio verificado correctamente.
Finished: SUCCESS
```

Esa salida demuestra que Jenkins puede clonar el proyecto. La URL es pública y no aparece ningún usuario, contraseña ni token.

## 5. Capturas recomendadas

| Captura | Dónde tomarla | Qué debe verse |
| --- | --- | --- |
| Configuración del pipeline | `gestor-incidencias-pipeline` → **Configurar** → sección **Pipeline** | `Pipeline script from SCM`, SCM `Git`, URL del repositorio, rama `*/main`, script `Jenkinsfile`. |
| Verificación de acceso | `verificar-acceso-github` → **Console Output** | `Cloning repository`, el commit descargado y `Finished: SUCCESS`. |
| Resultado del job | Página de `verificar-acceso-github` | Build verde y fecha de ejecución. |

Si `GITHUB_TOKEN` está vacío, en la configuración del job debe aparecer la credencial como `- none -`. Si algún día se usa token, la captura debe mostrar únicamente el identificador `github-credentials`, nunca su valor.

**No captures** el archivo `.env`, la pantalla de creación de credenciales con el token visible ni la contraseña del administrador.

## 6. Sobre el job principal y el agente

El job `gestor-incidencias-pipeline` queda configurado para leer el `Jenkinsfile` desde GitHub, pero el `Jenkinsfile` actual declara:

```groovy
agent {
    label 'gestor-incidencias'
}
```

Ese agente no existe en el Jenkins de `compose.jenkins.yaml`; es el que Uriel conectó en su servidor de laboratorio. Por eso:

- El job principal puede quedar en espera si se construye en este Jenkins.
- La comprobación de acceso se hace con `verificar-acceso-github`, que corre en el nodo integrado y no necesita ese agente.
- Para ejecutar el pipeline completo en este Jenkins habría que agregar un agente con la etiqueta `gestor-incidencias`.

## 7. Solución de problemas

| Síntoma | Causa probable | Solución |
| --- | --- | --- |
| En el log aparece `GITHUB_REPO_URL no está definida` | Compose no encontró el `.env` | Ejecuta los comandos desde la raíz del repositorio y revisa `docker compose config`. |
| Los jobs no aparecen | El volumen conserva los scripts viejos | Ejecuta `down -v` o elimina los scripts de `init.groovy.d` y reinicia. |
| `verificar-acceso-github` falla con `git: not found` | La imagen no tiene Git | Agrega `git` al `apt-get install` del `jenkins/Dockerfile` y reconstruye. |
| El pipeline principal queda en cola | No existe el agente `gestor-incidencias` | Usa el job de verificación o conecta un agente con esa etiqueta. |
| No se crea la credencial | `GITHUB_TOKEN` está vacío o falta `GITHUB_USER` | Revisa el `.env`; para un repositorio público no es necesaria. |
