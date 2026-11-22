pipeline {
    // Utilizar el agente exclusivo del proyecto grupal.
    agent {
        label 'gestor-incidencias'
    }

    // El pipeline se ejecuta solo cuando detecta cambios en el repositorio.
    triggers {
        pollSCM('H/5 * * * *')
    }

    environment {
        // La cadena de conexion se guarda como credencial en Jenkins,
        // nunca dentro del repositorio.
        TEST_DATABASE_URL = credentials('test-database-url')
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    stages {
        // Primera etapa: comprobar las herramientas del agente.
        stage('Verificar agente') {
            steps {
                sh '''
                    echo "Agente del Gestor de Incidencias funcionando"
                    python --version
                    git --version
                    java -version
                '''
            }
        }

        // Preparar un entorno virtual propio para no ensuciar el agente.
        stage('Instalar dependencias') {
            steps {
                sh '''
                    python -m venv .venv
                    . .venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        // La base de pruebas puede tardar en aceptar conexiones.
        stage('Esperar base de datos') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python - <<'PY'
import os, sys, time, psycopg

url = os.environ["TEST_DATABASE_URL"]
for intento in range(1, 31):
    try:
        psycopg.connect(url, connect_timeout=3).close()
        print("PostgreSQL de pruebas disponible")
        sys.exit(0)
    except Exception as error:
        print(f"Intento {intento}/30: la base aun no responde ({error})")
        time.sleep(2)
sys.exit("La base de pruebas no respondio despues de 60 segundos")
PY
                '''
            }
        }

        // Ejecutar las pruebas que ya existian en el repositorio.
        stage('Pruebas Pytest') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest --cov=app \
                           --cov-report=term-missing \
                           --cov-report=xml \
                           --junitxml=resultados-pruebas.xml
                '''
            }
        }
    }

    post {
        always {
            // Publicar el informe para verlo desde la interfaz de Jenkins.
            junit allowEmptyResults: true, testResults: 'resultados-pruebas.xml'
            archiveArtifacts artifacts: 'resultados-pruebas.xml, coverage.xml',
                             allowEmptyArchive: true
        }
        success {
            echo 'Las pruebas automatizadas se ejecutaron correctamente.'
        }
        failure {
            echo 'El pipeline fallo. Revisar la salida de la consola.'
        }
    }
}
