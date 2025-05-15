# projects/views.py

from django.shortcuts import render  # Vue HTML
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from .models import Project
from .serializers import ProjectSerializer
from .permissions import IsProjectOwner  # ✅ Import propre depuis fichier dédié


# ✅ VUE HTML (interface utilisateur classique)
# Affiche la page de création de projet (formulaire HTML, non-API)
def create_project_page(request):
    return render(request, 'core/create_project.html')


# ✅ API REST : Lister les projets ou en créer un nouveau (GET + POST)
class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsProjectOwner]

    def perform_create(self, serializer):
        # 🔐 On attribue automatiquement le client à l'utilisateur connecté
        serializer.save(client=self.request.user)


# ✅ API REST : Détail d'un projet (GET) + possibilité de mise à jour ou suppression (PUT, DELETE)
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsProjectOwner]

    def perform_update(self, serializer):
        # 🔒 Le champ client ne doit pas changer, on ne le met pas à jour
        serializer.save()

    def perform_destroy(self, instance):
        # 🔁 Supprime le projet (accessible au client ou admin)
        instance.delete()

# ✅ VUE HTML : Liste des projets disponibles (publics et actifs) pour les entrepreneurs
def find_jobs_view(request):
    # 🔍 On récupère uniquement les projets publics et encore actifs
    projects = Project.objects.filter(is_public=True, status='active').order_by('-created_at')

    # 📄 On passe la liste des projets à la page HTML dédiée
    return render(request, 'projects/project_list.html', {'projects': projects})

# ✅ Vue HTML pour voir les détails d’un projet
from django.shortcuts import render, get_object_or_404
from projects.models import Project
from bids.models import Bid

def project_detail_page(request, project_id):
    # 🔍 Récupération du projet
    project = get_object_or_404(Project, id=project_id)

    # ⚠️ Vérifie si l’entrepreneur connecté a déjà soumis une proposition
    has_already_bid = False
    if request.user.is_authenticated and getattr(request.user, 'is_contractor', False):
        has_already_bid = Bid.objects.filter(project=project, contractor=request.user).exists()

    # 🔁 Envoie les infos au template
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'has_already_bid': has_already_bid,
    })
