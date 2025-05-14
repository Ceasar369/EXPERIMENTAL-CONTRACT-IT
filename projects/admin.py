# projects/admin.py

# 🧩 Configuration de l'interface d'administration Django pour les projets publiés sur CONTRACT-IT

from django.contrib import admin
from .models import Project

# ⚙️ Configuration de l’interface admin pour les projets CONTRACT-IT
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # 📄 Champs affichés dans la liste des projets
    list_display = ('title', 'client', 'contractor', 'status', 'budget', 'deadline')

    # 🔍 Filtres disponibles dans la barre latérale
    list_filter = ('status', 'category')

    # 🔎 Champs sur lesquels la recherche admin peut s’appliquer
    search_fields = ('title', 'description', 'location')

