# ---------------------------------------------------------------------
# 📁 Fichier : bids/admin.py
#
# 🎯 Ce fichier configure l’interface d’administration Django
#     pour la gestion des propositions (bids) soumises par les entrepreneurs.
#
# Chaque bid correspond à une offre envoyée par un entrepreneur
# pour un projet publié sur la plateforme CONTRACT-IT.
#
# L’objectif ici est d’afficher dans l’admin :
#     - la liste des bids,
#     - leurs détails clés : projet, entrepreneur, statut, budget, message...
#     - d’ajouter des filtres pour faciliter la modération manuelle.
#
# 👉 L’interface admin est utile pour surveiller l’activité de la plateforme,
#     détecter des abus, ou gérer manuellement certaines offres si besoin.
# ---------------------------------------------------------------------

# 🔁 Import principal du module admin de Django
from django.contrib import admin

# 📦 Import du modèle Bid défini dans models.py
from .models import Bid


# ---------------------------------------------------------------------
# ⚙️ Configuration personnalisée pour le modèle Bid dans l’admin
# ---------------------------------------------------------------------
@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    """
    Interface Django Admin pour le modèle Bid.

    Affiche les offres dans l’administration avec :
    - les colonnes importantes dans la liste,
    - des filtres par statut ou par projet,
    - un champ de recherche.
    """

    # ✅ Champs visibles dans la vue liste (tableau de tous les bids)
    list_display = ('project', 'contractor', 'amount', 'status', 'created_at')

    # 🔍 Filtres disponibles dans la sidebar de l’admin
    list_filter = ('status', 'created_at', 'project')

    # 🔎 Champs sur lesquels la barre de recherche admin peut s’appliquer
    search_fields = ('project__title', 'contractor__username', 'message')

    # 📅 Tri par défaut (les plus récents d’abord)
    ordering = ('-created_at',)
