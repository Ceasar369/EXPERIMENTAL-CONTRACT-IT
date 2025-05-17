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
# ⚙️ Configuration personnalisée pour le modèle Bid dans l’interface Django Admin
# ---------------------------------------------------------------------
@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    """
    Interface Django Admin pour le modèle Bid.

    🧾 Affiche les offres (bids) dans l’administration avec :
        - colonnes personnalisées dans la vue liste (`list_display`)
        - filtres utiles dans la barre latérale (`list_filter`)
        - barre de recherche sur plusieurs champs (`search_fields`)
        - tri par défaut sur la date de création (le plus récent en premier)
    """

    # ✅ Colonnes visibles dans la vue tableau admin
    list_display = (
        'project',       # 🔗 Projet concerné
        'contractor',    # 👤 Entrepreneur ayant soumis l'offre
        'amount',        # 💰 Montant proposé
        'status',        # 📌 Statut (en attente, accepté, refusé...)
        'created_at'     # 🗓️ Date de soumission
    )

    # 🔍 Filtres rapides dans la sidebar
    list_filter = (
        'status',        # Statut de la bid (filtrage rapide)
        'created_at',    # Mois/année de création
        'project'        # Nom du projet
    )

    # 🔎 Champs accessibles par la barre de recherche admin
    search_fields = (
        'project__title',        # Recherche par titre de projet
        'contractor__username',  # Recherche par nom d’utilisateur de l’entrepreneur
        'message'                # Recherche par contenu de l’offre
    )

    # 📅 Tri automatique : les plus récentes en haut
    ordering = ('-created_at',)
