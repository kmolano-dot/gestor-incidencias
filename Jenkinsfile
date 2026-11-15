
pipeline {
    // Utilizar el agente exclusivo del proyecto grupal.
    agent {
        label 'gestor-incidencias'
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
    }
}
