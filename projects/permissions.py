# projects/permissions.py

from rest_framework.permissions import BasePermission

# 📛 Permission : Seul le propriétaire du projet ou un admin peut modifier/supprimer
class IsProjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.client or request.user.is_staff
