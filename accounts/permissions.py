# accounts/permissions.py

# 🔒 Permissions personnalisées CONTRACT-IT basées sur le rôle utilisateur (client vs entrepreneur)

from rest_framework.permissions import BasePermission

# ✅ Permission : l'utilisateur doit être un entrepreneur connecté
class IsContractor(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_contractor

# ✅ Permission : l'utilisateur doit être un client connecté
class IsClient(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_client

# ✅ Autorise client OU entrepreneur (utile pour créer un projet)
class IsClientOrContractor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user and user.is_authenticated and (user.is_client or user.is_contractor)
