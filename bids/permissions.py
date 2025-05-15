# bids/permissions.py

from rest_framework import permissions
from projects.models import Project

# 🔒 Permission pour s'assurer que l'utilisateur est un entrepreneur
class IsContractor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_contractor


# 🔐 Permission pour s'assurer que l'utilisateur est le client propriétaire du projet
class IsProjectOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_id')
        try:
            project = Project.objects.get(id=project_id)
            return project.client == request.user
        except Project.DoesNotExist:
            return False
