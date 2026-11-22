# Imagen de Jenkins preparada para ejecutar las pruebas del proyecto.
# La imagen oficial no trae Python, que es necesario para Pytest.
FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        libpq-dev && \
    ln -s /usr/bin/python3 /usr/local/bin/python && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER jenkins

# Plugins necesarios para el pipeline y la publicacion de resultados.
RUN jenkins-plugin-cli --plugins \
    workflow-aggregator \
    git \
    github \
    junit \
    credentials-binding \
    timestamper
