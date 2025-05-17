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

# ---------------------------------------------------------------------
# 📦 IMPORTS DJANGO
# ---------------------------------------------------------------------
from django.urls import path

# ---------------------------------------------------------------------
# 📦 IMPORTS DES VUES HTML DE L’APP PROJECTS
# ---------------------------------------------------------------------
from .views import (
    create_project_page_view,             # ✅ Créer un nouveau projet (client)
    find_jobs_view,                       # ✅ Voir les projets disponibles (entrepreneur)
    project_detail_page_view,             # ✅ Voir les détails d’un projet
    my_projects_view,                     # ✅ Voir mes projets publiés (client)
    awarded_projects_view,                # ✅ Voir les projets qui m’ont été attribués (entrepreneur)
    edit_project_view,                    # ✅ Modifier un projet déjà publié (client)
    
    # 📁 Portfolio externe (entrepreneur)
    add_external_portfolio_view,          # ✅ Ajouter un projet externe au portfolio
    external_portfolio_detail_view,       # ✅ Détail public d’un projet externe

    # 📁 Portfolio interne (CONTRACT-IT)
    internal_portfolio_detail_view,       # ✅ Détail public d’un projet interne (de la plateforme)
    toggle_internal_portfolio_view        # ✅ Activer/désactiver un projet dans le portfolio
)

# ---------------------------------------------------------------------
# 🌐 Liste des routes disponibles pour l’application `projects`
# ---------------------------------------------------------------------
urlpatterns = [

    # -----------------------------------------------------------------
    # 📝 1. Créer un nouveau projet (client connecté)
    # URL : /projects/create/
    # Vue : create_project_page_view
    # -----------------------------------------------------------------
    path('create/', create_project_page_view, name='create_project_view'),

    # -----------------------------------------------------------------
    # 🔍 2. Afficher les projets publics disponibles (entrepreneurs)
    # URL : /projects/jobs/
    # Vue : find_jobs_view
    # -----------------------------------------------------------------
    path('jobs/', find_jobs_view, name='find_jobs_view'),

    # -----------------------------------------------------------------
    # 📄 3. Détails d’un projet donné
    # URL : /projects/details/12/
    # Vue : project_detail_page_view
    # -----------------------------------------------------------------
    path('details/<int:project_id>/', project_detail_page_view, name='project_detail_page_view'),

    # -----------------------------------------------------------------
    # 📋 4. Mes projets (client connecté)
    # URL : /projects/my-projects/
    # Vue : my_projects_view
    # -----------------------------------------------------------------
    path('my-projects/', my_projects_view, name='my_projects_view'),

    # -----------------------------------------------------------------
    # 🛠️ 5. Projets attribués à un entrepreneur (dashboard entrepreneur)
    # URL : /projects/awarded/
    # Vue : awarded_projects_view
    # -----------------------------------------------------------------
    path('awarded/', awarded_projects_view, name='awarded_projects_view'),

    # -----------------------------------------------------------------
    # ✏️ 6. Modifier un projet existant (client uniquement)
    # URL : /projects/edit/12/
    # Vue : edit_project_view
    # -----------------------------------------------------------------
    path('edit/<int:project_id>/', edit_project_view, name='edit_project_view'),

    # -----------------------------------------------------------------
    # 🧱 7. Ajouter un projet externe au portfolio (entrepreneur)
    # URL : /projects/portfolio/add/
    # Vue : add_external_portfolio_view
    # -----------------------------------------------------------------
    path('portfolio/add/', add_external_portfolio_view, name='add_external_portfolio_view'),

    # -----------------------------------------------------------------
    # 🖼️ 8. Voir un projet EXTERNE dans le portfolio public
    # URL : /projects/portfolio/external/23/
    # Vue : external_portfolio_detail_view
    # -----------------------------------------------------------------
    path('portfolio/external/<int:portfolio_id>/', external_portfolio_detail_view, name='external_portfolio_detail_view'),

    # -----------------------------------------------------------------
    # 🖼️ 9. Voir un projet INTERNE CONTRACT-IT dans le portfolio public
    # URL : /projects/portfolio/internal/17/
    # Vue : internal_portfolio_detail_view
    # -----------------------------------------------------------------
    path('portfolio/internal/<int:project_id>/', internal_portfolio_detail_view, name='internal_portfolio_detail_view'),

    # -----------------------------------------------------------------
    # 🔁 10. Activer ou désactiver un projet dans le portfolio
    # URL : /projects/portfolio/internal/toggle/17/
    # Vue : toggle_internal_portfolio_view
    # -----------------------------------------------------------------
    path('portfolio/internal/toggle/<int:project_id>/', toggle_internal_portfolio_view, name='toggle_internal_portfolio_view'),
]
