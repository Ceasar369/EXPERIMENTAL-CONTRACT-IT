# 📁 Fichier : accounts/admin.py
# 🎛️ Ce fichier configure l'interface d'administration Django pour le projet CONTRACT-IT.
# Il sépare les utilisateurs selon leur rôle :
#   - Superadmins (comptes techniques pour gérer la plateforme),
#   - Utilisateurs qui publient des projets (clients),
#   - Utilisateurs qui proposent leurs services (entrepreneurs).
# Certains utilisateurs peuvent avoir un double rôle (client + entrepreneur).
# Ce fichier permet d’en afficher clairement la distinction dans l’interface admin Django.

from django.contrib import admin                          # 📦 Module principal pour configurer /admin
from django.contrib.auth.admin import UserAdmin           # 🎛️ Comportement par défaut des utilisateurs admin
from .models import CustomUser                            # 👤 Modèle utilisateur CONTRACT-IT

# --------------------------------------------------------------------------------
# 🔎 Fonction utilitaire pour détecter un double rôle (client + entrepreneur)
# Elle sera utilisée dans l’interface admin pour repérer les utilisateurs hybrides
# --------------------------------------------------------------------------------
def is_dual_user(obj):
    """Affiche True si l'utilisateur est à la fois client ET entrepreneur"""
    return obj.is_client and obj.is_contractor

# ✅ Affiche une icône ✓ ou ✗ dans la colonne
is_dual_user.boolean = True
# ✅ Titre de la colonne dans /admin
is_dual_user.short_description = "Client + Entrepreneur"

# --------------------------------------------------------------------------------
# 🔀 VERSION FUSIONNÉE : UN SEUL ADMIN POUR CustomUser
# On adapte dynamiquement l’affichage selon le rôle de l’utilisateur :
# - Si superadmin → vue technique
# - Si client → vue client avec ses champs
# - Si entrepreneur → vue entrepreneur avec ses champs
# Cette stratégie permet d’éviter le bug `AlreadyRegistered`.
# --------------------------------------------------------------------------------

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # ✅ Liste personnalisée (sans 'username' qui a été supprimé)
    list_display = (
        'email', 'first_name', 'last_name',
        'is_client', 'is_contractor', 'is_verified', 'is_active',
        'is_staff', is_dual_user  # ➕ Colonne booléenne personnalisée
    )

    # ✅ Ajout de filtres dans la barre latérale pour trier rapidement
    list_filter = (
        'is_client', 'is_contractor', 'is_verified', 'is_active'
    )

    # 🕓 Champs affichés en lecture seule
    readonly_fields = ('date_joined',)

    # 🔍 Barre de recherche dans l’interface admin
    search_fields = ('email', 'city')

    # 🧭 Tri par défaut dans la liste des utilisateurs
    ordering = ('email',)

    def get_queryset(self, request):
        """
        🔁 Récupère tous les utilisateurs pour affichage.
        Triés par adresse courriel, sans filtrage particulier.
        """
        return super().get_queryset(request).order_by('email')

    def get_fieldsets(self, request, obj=None):
        """
        🧩 Affiche dynamiquement les champs à éditer selon le type d’utilisateur affiché.
        """
        if obj and obj.is_superuser:
            return (
                (None, {'fields': ('email', 'password')}),
                ('Informations personnelles', {'fields': ()}),
                ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
                ('Dates importantes', {'fields': ('last_login',)}),
            )

        elif obj and obj.is_client:
            return (
                (None, {'fields': ('email', 'password')}),
                ('Profil client CONTRACT-IT', {
                    'fields': (
                        'first_name', 'last_name',
                        'phone', 'city', 'language', 'company_name',
                        'project_history_count', 'is_verified'
                    )
                }),
                ('Permissions', {'fields': ('is_active',)}),
                ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
            )

        elif obj and obj.is_contractor:
            return (
                (None, {'fields': ('email', 'password')}),
                ('Profil entrepreneur CONTRACT-IT', {
                    'fields': (
                        'first_name', 'last_name',
                        'phone', 'city', 'language', 'profile_picture', 'bio',
                        'specialties', 'hourly_rate', 'availability',
                        'certifications', 'company_name', 'is_verified'
                    )
                }),
                ('Permissions', {'fields': ('is_active',)}),
                ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
            )

        return super().get_fieldsets(request, obj)

    def get_add_fieldsets(self, request):
        """
        🆕 Affichage du formulaire de création dans l'admin (ajouter un utilisateur)
        On inclut les rôles pour affectation directe à la création.
        """
        return (
            (None, {
                'classes': ('wide',),
                'fields': (
                    'email', 'password1', 'password2',
                    'first_name', 'last_name',
                    'is_staff', 'is_superuser', 'is_client', 'is_contractor'
                ),
            }),
        )
