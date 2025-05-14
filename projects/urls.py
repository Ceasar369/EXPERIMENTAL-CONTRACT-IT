# projects/urls.py

from django.urls import path
from .views import (
    create_project_page,            # Vue HTML
    ProjectListCreateView,          # API REST - GET/POST
    ProjectDetailView               # API REST - GET/PUT/DELETE
)

urlpatterns = [
    # 🌐 Vue HTML - Page de création de projet (formulaire pour interface classique)
    path('create/', create_project_page, name='create-project'),

    # 🔌 API REST - Liste tous les projets ou en créer un nouveau
    path('', ProjectListCreateView.as_view(), name='project-list-create'),

    # 🔍 API REST - Affiche/modifie/supprime un projet spécifique
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
]
