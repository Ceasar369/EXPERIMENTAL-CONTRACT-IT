# projects/views.py

from django.shortcuts import render  # Vue HTML
from rest_framework import generics, permissions
from .models import Project
from .serializers import ProjectSerializer
from rest_framework.permissions import BasePermission

# ✅ VUE HTML (interface utilisateur classique)
# Affiche la page de création de projet (formulaire HTML, non-API)
def create_project_page(request):
    return render(request, 'core/create_project.html')

# 📛 Seul le client propriétaire peut modifier ou supprimer son projet
class IsProjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.client or request.user.is_staff

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

