# projects/urls.py

from django.urls import path
from .views import (
    create_project_page,            # Vue HTML
    find_jobs_view,                 # ✅ Vue HTML - Liste des projets publics (NEW)
    ProjectListCreateView,          # API REST - GET/POST
    ProjectDetailView,               # API REST - GET/PUT/DELETE
    project_detail_page  # Vue HTML classique
)

urlpatterns = [
    # 🌐 Vue HTML - Page de création de projet (formulaire pour interface classique)
    path('create/', create_project_page, name='create-project'),

    # 💼 Vue HTML - Affiche la liste des projets publics disponibles (pour entrepreneurs)
    path('jobs/', find_jobs_view, name='find_jobs'),

    # 🔌 API REST - Liste tous les projets ou en créer un nouveau
    path('', ProjectListCreateView.as_view(), name='project-list-create'),

    # 🔍 API REST - Affiche/modifie/supprime un projet spécifique
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),

    # 🔍 Vue HTML - Détail d’un projet spécifique (interface utilisateur)
    path('details/<int:project_id>/', project_detail_page, name='project_detail_html'),

]
