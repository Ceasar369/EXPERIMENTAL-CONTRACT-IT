# ---------------------------------------------------------------------
# 📁 Fichier : projects/admin.py
#
# 🧩 Interface d'administration Django pour les projets CONTRACT-IT
#
# Ce fichier configure comment les projets publiés par les clients
# sont affichés, filtrés et recherchés dans le panneau d’administration.
#
# ➕ Avantage : permet aux administrateurs ou modérateurs du site de :
#    - Voir rapidement les projets créés,
#    - Filtrer selon statut ou catégorie,
#    - Rechercher un projet par titre, description ou localisation,
#    - Éventuellement modifier ou supprimer un projet en cas de litige.
#
# Ce fichier est totalement indépendant des API ou des sessions utilisateurs.
# Il sert exclusivement à l'interface `/admin/`.
# ---------------------------------------------------------------------

# 🔁 Import du système admin de Django
from django.contrib import admin

# 📦 Import du modèle Project défini dans models.py
from .models import Project

# ---------------------------------------------------------------------
# 🔧 Personnalisation de l'affichage du modèle Project dans l'admin
# ---------------------------------------------------------------------
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Classe de configuration pour l’affichage des projets dans l’admin.
    Elle permet de définir quels champs s'affichent, comment filtrer,
    et quels champs peuvent être recherchés.
    """

    # 📄 Champs visibles dans la liste des projets (dans /admin/projects/project/)
    list_display = (
        'title',           # Titre du projet
        'client',          # Client qui l’a créé
        'contractor',      # Entrepreneur attribué (peut être vide)
        'status',          # Statut actuel (actif, en cours, terminé…)
        'budget',          # Budget prévu
        'deadline',         # Date limite du projet
        'milestone_count'  # Nombre total de jalons associés
    )

    # 🧭 Filtres disponibles dans la colonne de droite
    list_filter = (
        'status',      # Filtrer les projets par statut
        'category'     # Filtrer par type de spécialité (ex : toiture, plomberie…)
    )

    # 🔍 Champs utilisés pour la recherche rapide via barre en haut
    search_fields = (
        'title',        # Permet de retrouver un projet par son nom
        'description',  # Recherche dans la description complète
        'location'      # Recherche par ville, région ou code postal
    )
