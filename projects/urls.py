# ---------------------------------------------------------------------
# 📁 Fichier : projects/urls.py
#
# 🗺️ Routes de l'application `projects` (interface HTML classique)
#
# Ce fichier regroupe toutes les URLs liées à la gestion des projets :
#    - création, affichage, édition,
#    - projets publiés par un client,
#    - projets attribués à un entrepreneur.
#
# Il ne contient aucune logique API, JWT ou REST.
# Chaque route est associée à une vue HTML, pensée pour les clients ou les entrepreneurs.
# ---------------------------------------------------------------------

# 🔁 Import standard de Django
from django.urls import path

# 🔁 Import des vues utilisées
from .views import (
    create_project_page,            # Créer un nouveau projet
    find_jobs_view,                 # Voir les projets disponibles (côté entrepreneur)
    project_detail_page,           # Voir les détails d’un projet
    my_projects_view,              # Voir les projets que j’ai publiés (client)
    awarded_projects_view,      # Voir les projets qu’on m’a attribués (entrepreneur)
    edit_project_view,             # Modifier un projet (client)
)

# ---------------------------------------------------------------------
# 🌐 Liste des routes disponibles
# ---------------------------------------------------------------------
urlpatterns = [
    # -----------------------------------------------------------------
    # 📝 1. Créer un nouveau projet (client)
    # Ex : /projects/create/
    # -----------------------------------------------------------------
    path('create/', create_project_page, name='create-project'),

    # -----------------------------------------------------------------
    # 🔍 2. Liste des projets disponibles à postuler (entrepreneurs)
    # Ex : /projects/jobs/
    # Affiche uniquement les projets actifs et publics
    # -----------------------------------------------------------------
    path('jobs/', find_jobs_view, name='find_jobs'),

    # -----------------------------------------------------------------
    # 📄 3. Détails d’un projet spécifique (accessible à tous les connectés)
    # Ex : /projects/details/12/
    # -----------------------------------------------------------------
    path("details/<int:project_id>/", project_detail_page, name="project-details"),

    # -----------------------------------------------------------------
    # 📋 4. Liste de mes projets (client connecté)
    # Ex : /projects/my-projects/
    # Permet de gérer ses propres projets (éditer, suivre, supprimer…)
    # -----------------------------------------------------------------
    path('my-projects/', my_projects_view, name='my_projects'),

    # -----------------------------------------------------------------
    # 🛠️ 5. Liste des projets qu’on m’a attribués (entrepreneur connecté)
    # Ex : /projects/awarded/
    # Permet de suivre l’avancement, les jalons, les documents…
    # -----------------------------------------------------------------
    path('awarded/', awarded_projects_view, name='awarded_projects'),

    # -----------------------------------------------------------------
    # ✏️ 6. Modifier un projet existant (client seulement, projet non attribué)
    # Ex : /projects/edit/12/
    # -----------------------------------------------------------------
    path("edit/<int:project_id>/", edit_project_view, name="edit-project"),
]
