# ---------------------------------------------------------------------
# 📁 Fichier : bids/urls.py
#
# 🎯 Ce fichier définit les routes URL de l’application `bids`.
#     Chaque route correspond à une **vue HTML classique** (pas d’API ici).
#
# Ces vues permettent aux utilisateurs de :
#     - soumettre une offre pour un projet (submit),
#     - voir une page de confirmation après soumission,
#     - consulter toutes les offres reçues pour un projet (client),
#     - accepter une proposition,
#     - voir ses propres bids.
#
# Les routes sont activées à travers l’inclusion dans `urls.py` principal.
# ---------------------------------------------------------------------

from django.urls import path
from .views import (
    SubmitBidFormView,
    bid_confirmation_view,
    project_bids_view,
    my_bids_view,
    accept_bid_view,
    bid_accepted_confirmation_view
)

app_name = "bids"

# ---------------------------------------------------------------------
# 🔗 Liste des routes disponibles pour les soumissions (bids)
# ---------------------------------------------------------------------
urlpatterns = [

    # 1️⃣ Soumettre une bid (formulaire GET + POST)
    # 🔐 Accessible uniquement à un entrepreneur connecté
    path(
        "submit/<int:project_id>/",           # Exemple : /bids/submit/5/
        SubmitBidFormView.as_view(),
        name="submit_bid_view"
    ),

    # 2️⃣ Confirmation après soumission
    # ✅ Redirigé ici après POST réussi
    path(
        "confirmation/",
        bid_confirmation_view,
        name="bid_confirmation_view"
    ),

    # 3️⃣ Voir toutes les offres reçues pour un projet (côté client)
    # 🔐 Seul le client propriétaire peut y accéder
    path(
        "view_bids/<int:project_id>/",        # Exemple : /bids/view_bids/5/
        project_bids_view,
        name="project_bids_view"
    ),

    # 4️⃣ Voir toutes les bids soumises par l’entrepreneur connecté
    # 🔐 Accessible depuis le tableau de bord contractor
    path(
        "my_bids/",
        my_bids_view,
        name="my_bids_view"
    ),

    # 5️⃣ Accepter une bid spécifique (côté client)
    path(
        "accept/<int:bid_id>/",
        accept_bid_view,
        name="accept_bid_view"
    ),

    # 6️⃣ Confirmation après acceptation d'une bid
    path(
        "accepted/confirmation/",
        bid_accepted_confirmation_view,
        name="bid_accepted_confirmation_view"
    ),
]
