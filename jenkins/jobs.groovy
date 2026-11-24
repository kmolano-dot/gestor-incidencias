import com.cloudbees.plugins.credentials.CredentialsScope
import com.cloudbees.plugins.credentials.SystemCredentialsProvider
import com.cloudbees.plugins.credentials.domains.Domain
import com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl
import hudson.model.FreeStyleProject
import hudson.plugins.git.BranchSpec
import hudson.plugins.git.GitSCM
import hudson.plugins.git.UserRemoteConfig
import hudson.tasks.Shell
import jenkins.model.Jenkins
import org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition
import org.jenkinsci.plugins.workflow.job.WorkflowJob

// Configuración leída desde el archivo .env (Compose la inyecta como variables de entorno).
def env = System.getenv()
def repoUrl = env['GITHUB_REPO_URL']?.trim()
def branch = env['GITHUB_BRANCH']?.trim() ?: 'main'
def githubUser = env['GITHUB_USER']?.trim()
def githubToken = env['GITHUB_TOKEN']?.trim()

if (!repoUrl) {
    println '[init] GITHUB_REPO_URL no está definida; no se crean los jobs de GitHub.'
    return
}

// Si hay token, se crea una credencial en Jenkins usando el ID fijo "github-credentials".
// El token nunca se escribe en el repositorio ni se muestra en la interfaz.
def credentialsId = null
if (githubToken) {
    credentialsId = 'github-credentials'
    try {
        def store = SystemCredentialsProvider.getInstance().getStore()
        def existing = store.getCredentials(Domain.global()).find { it.id == credentialsId }
        if (existing != null) {
            store.removeCredentials(Domain.global(), existing)
        }
        store.addCredentials(
            Domain.global(),
            new UsernamePasswordCredentialsImpl(
                CredentialsScope.GLOBAL,
                credentialsId,
                'Credencial de GitHub leída desde .env',
                githubUser ?: 'git',
                githubToken
            )
        )
        SystemCredentialsProvider.getInstance().save()
        println "[init] Credencial '${credentialsId}' creada desde .env."
    } catch (Exception e) {
        println "[init] No se pudo crear la credencial de GitHub: ${e.message}"
        credentialsId = null
    }
} else {
    println '[init] GITHUB_TOKEN vacío; el repositorio se consultará de forma anónima.'
}

// Se crea un GitSCM nuevo para cada job para no compartir la misma instancia.
def buildScm = {
    new GitSCM(
        [new UserRemoteConfig(repoUrl, null, null, credentialsId)],
        [new BranchSpec("*/${branch}")],
        false,
        [],
        null,
        null,
        []
    )
}

def jenkins = Jenkins.get()

// ---------------------------------------------------------------------------
// Job principal: lee el Jenkinsfile directamente desde GitHub.
// ---------------------------------------------------------------------------
def pipelineName = 'gestor-incidencias-pipeline'
def pipelineJob = jenkins.getItem(pipelineName)
if (pipelineJob == null) {
    pipelineJob = jenkins.createProject(WorkflowJob, pipelineName)
} else if (!(pipelineJob instanceof WorkflowJob)) {
    println "[init] El job '${pipelineName}' existe pero no es un Pipeline; no se modifica."
    pipelineJob = null
}
if (pipelineJob != null) {
    def definition = new CpsScmFlowDefinition(buildScm(), 'Jenkinsfile')
    definition.setLightweight(true)
    pipelineJob.setDefinition(definition)
    pipelineJob.setDescription(
        "Pipeline del Gestor de Incidencias. Lee el Jenkinsfile desde ${repoUrl} (rama ${branch})."
    )
    pipelineJob.save()
    println "[init] Job '${pipelineName}' configurado para leer ${repoUrl} (rama ${branch})."
}

// ---------------------------------------------------------------------------
// Job de verificación: clona el repositorio en el nodo integrado y muestra el
// commit descargado. No necesita el agente 'gestor-incidencias'.
// ---------------------------------------------------------------------------
def verifyName = 'verificar-acceso-github'
def verifyJob = jenkins.getItem(verifyName)
if (verifyJob == null) {
    verifyJob = jenkins.createProject(FreeStyleProject, verifyName)
} else if (!(verifyJob instanceof FreeStyleProject)) {
    println "[init] El job '${verifyName}' existe pero no es Freestyle; no se modifica."
    verifyJob = null
}
if (verifyJob != null) {
    def verifyScript = """#!/bin/sh
set -eu
echo "Repositorio: ${repoUrl}"
echo "Rama configurada: ${branch}"
echo "Commit descargado:"
git log -1 --format='  Hash:    %H%n  Autor:   %an%n  Mensaje: %s'
echo "Acceso al repositorio verificado correctamente."
"""
    verifyJob.setScm(buildScm())
    verifyJob.getBuildersList().clear()
    verifyJob.getBuildersList().add(new Shell(verifyScript))
    verifyJob.setDescription(
        'Comprueba que Jenkins puede clonar el repositorio del Gestor de Incidencias.'
    )
    verifyJob.save()
    println "[init] Job '${verifyName}' configurado para verificar el acceso al repositorio."
}
