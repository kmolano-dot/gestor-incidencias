import jenkins.model.*
import hudson.security.*

def adminUser = System.getenv("JENKINS_ADMIN_USER")
def adminPassword = System.getenv("JENKINS_ADMIN_PASSWORD")

if (!adminUser || !adminPassword) {
    throw new IllegalStateException("Faltan las variables JENKINS_ADMIN_USER y/o JENKINS_ADMIN_PASSWORD")
}

def instance = Jenkins.getInstance()
def hudsonRealm = new HudsonPrivateSecurityRealm(false)
hudsonRealm.createAccount(adminUser, adminPassword)
instance.setSecurityRealm(hudsonRealm)

def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
strategy.setAllowAnonymousRead(false)
instance.setAuthorizationStrategy(strategy)
instance.save()