# accounts/admin.py

# 🎛️ Interface d'administration Django personnalisée pour les utilisateurs et portfolios CONTRACT-IT

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ExternalPortfolioItem, InternalPortfolioItem


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_client', 'is_contractor', 'is_staff')
    list_filter = ('is_client', 'is_contractor', 'is_staff')

    # ✅ On affiche la date_joined en lecture seule
    readonly_fields = ('date_joined',)

    # ✅ Champs affichés lors de l'ajout d’un nouvel utilisateur
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_client', 'is_contractor'),
        }),
    )

    # ✅ Champs personnalisés uniquement (aucun champ déjà dans UserAdmin par défaut)
    fieldsets = UserAdmin.fieldsets + (
        ('Informations CONTRACT-IT', {
            'fields': (
                'phone', 'profile_picture', 'bio', 'city', 'language',
                'is_verified', 'is_client', 'is_contractor',
                'specialties', 'hourly_rate', 'availability', 'certifications',
                'company_name', 'project_history_count'
            )
        }),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)


@admin.register(ExternalPortfolioItem)
class ExternalPortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')


@admin.register(InternalPortfolioItem)
class InternalPortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'created_at')
