# Guía de colaboración

El repositorio del equipo es [gestor-incidencias](https://github.com/kmolano-dot/gestor-incidencias). Antes de comenzar, acepta la invitación y verifica que puedes acceder.

## Flujo propuesto

1. Clona el repositorio y actualiza la rama principal:

   ```bash
   git clone https://github.com/kmolano-dot/gestor-incidencias.git
   cd gestor-incidencias
   git switch main
   git pull origin main
   ```

2. Crea una rama para tu trabajo. Por ejemplo:

   ```bash
   git switch -c feature/registro-consulta-incidencias
   ```

3. Realiza tus cambios, revísalos con `git status` y crea un commit descriptivo:

   ```bash
   git add .
   git commit -m "Agregar aplicación Flask"
   git push -u origin feature/registro-consulta-incidencias
   ```

4. En GitHub, abre un **pull request** desde tu rama hacia `main`. Explica qué agregaste y cómo se puede comprobar. Pide a un compañero que lo revise y, una vez aprobado por el equipo, intégralo.
5. Después de integrar, actualiza tu copia de `main` antes de empezar otra tarea. Si tu rama quedó desactualizada mientras trabajabas, coordina la resolución de conflictos con el equipo.

Cada integrante debe hacer sus propios commits con su cuenta de GitHub para que sus aportes queden identificados. Antes de hacer `git add .`, revisa que no estés incluyendo contraseñas, archivos de entorno, bases de datos locales ni otros archivos que no deban compartirse.

## Nombres de ramas y reparto

Usen nombres que describan el cambio. Los prefijos `feature/`, `fix/`, `test/` y `docs/` pueden ayudar a identificar si se trata de una funcionalidad, una corrección, pruebas o documentación. Son una orientación, no una regla obligatoria: el nombre puede variar según el trabajo.

| Responsable | Trabajo | Rama sugerida |
| --- | --- | --- |
| Uriel | Aplicación y estructura del proyecto | `feature/registro-consulta-incidencias` |
| Lina | Base de datos PostgreSQL | `feature/modelo-datos-postgresql` |
| Jorge | Docker y comunicación entre contenedores | `feature/contenedores-flask-postgresql` |
| Diego | Pruebas automatizadas | `test/operaciones-incidencias` |
| Kevin | Organización, documentación y evidencias | `docs/guia-trabajo-colaborativo` |

Estas ramas son una propuesta para acordar con el equipo. Conviene que Uriel suba primero la aplicación para facilitar la integración y las pruebas; Lina puede avanzar en paralelo y Jorge y Diego coordinar sus cambios con el código disponible.

## Evidencias

Conserva los enlaces de los pull requests y capturas de las ramas, commits y revisiones que realmente se hagan. Cada integrante documenta su proceso en el documento compartido. No se deben registrar como completadas las actividades que aún estén pendientes.
