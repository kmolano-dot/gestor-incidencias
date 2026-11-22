# Partimos de la imagen oficial LTS de Jenkins
FROM jenkins/jenkins:lts

# Cambiamos a usuario root para instalar el cliente de Docker
USER root

RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Volvemos al usuario seguro por defecto de Jenkins
USER jenkins

# Saltamos el asistente inicial de configuración (el de la contraseña temporal)
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"

# Preinstalamos automáticamente todos los plugins que necesita el equipo
RUN jenkins-plugin-cli --plugins \
    git \
    github \
    workflow-aggregator \
    docker-workflow \
    docker-plugin

# Copiar script de creación de usuario
COPY security.groovy /usr/share/jenkins/ref/init.groovy.d/security.groovy