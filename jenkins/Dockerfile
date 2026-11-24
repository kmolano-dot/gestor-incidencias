# Partimos de la imagen oficial LTS de Jenkins
FROM jenkins/jenkins:lts

# Cambiamos a usuario root para instalar el cliente de Docker
USER root

RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Python es necesario para ejecutar las pruebas con Pytest dentro del pipeline.
# libpq-dev permite instalar el conector de PostgreSQL.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        libpq-dev && \
    ln -s /usr/bin/python3 /usr/local/bin/python && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Volvemos al usuario seguro por defecto de Jenkins
USER jenkins

# Saltamos el asistente inicial de configuración (el de la contraseña temporal)
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"

# Preinstalamos automáticamente todos los plugins que necesita el equipo.
# junit, credentials-binding y timestamper los usa el pipeline de pruebas.
RUN jenkins-plugin-cli --plugins \
    git \
    github \
    workflow-aggregator \
    docker-workflow \
    docker-plugin \
    junit \
    credentials-binding \
    timestamper

# Copiar script de creación de usuario
COPY security.groovy /usr/share/jenkins/ref/init.groovy.d/security.groovy
