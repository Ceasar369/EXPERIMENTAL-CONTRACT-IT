# ---------------------------------------------------------------------
# 📁 Fichier : bids/urls.py
#
# 🎯 Ce fichier définit les routes URL de l’application `bids`.
# Chaque route correspond à une **vue HTML classique** (pas d’API ici).
#
# Ces vues permettent aux utilisateurs de :
#     - soumettre une offre pour un projet (submit),
#     - voir une page de confirmation après soumission,
#     - consulter toutes les offres reçues pour un projet (client),
#
# Les routes sont activées à travers l’inclusion dans `urls.py` principal.
# ---------------------------------------------------------------------

# 🔁 Import de la fonction path pour déclarer les routes
from django.urls import path
from . import views

# 🔁 Import des vues associées
from .views import (
    SubmitBidFormView,
    accept_bid_view,
    bid_accepted_confirmation,         # ✅ Vue GET/POST de soumission
    bid_confirmation_view,     # ✅ Vue simple : message de confirmation
    project_bids_view,         # ✅ Vue : voir toutes les bids d’un projet (client)
    my_bids_view               # ✅ Vue : voir les bids soumises par l’entrepreneur
)


# ---------------------------------------------------------------------
# 🔗 Liste des routes disponibles pour les soumissions (bids)
# ---------------------------------------------------------------------
urlpatterns = [

    # 🔹 Soumettre une bid (formulaire GET + POST)
    # 🧑‍🔧 Vue utilisée par un entrepreneur intéressé par un projet public
    path(
        "submit/<int:project_id>/",           # Ex: /bids/submit/5/
        SubmitBidFormView.as_view(),
        name="submit-bid"
    ),

    # 🔹 Confirmation visuelle après la soumission
    # ✅ L’utilisateur est redirigé ici après avoir soumis une offre
    path(
        "confirmation/",
        bid_confirmation_view,
        name="bid-confirmation"
    ),

    # 🔹 Voir toutes les offres reçues pour un projet donné
    # 👤 Accessible uniquement au client qui a publié ce projet
    path(
        "view-bids/<int:project_id>/",        # Ex: /bids/view-bids/5/
        project_bids_view,
        name="view-project-bids"
    ),

    # 🔹 Voir toutes les bids soumises par l’entrepreneur connecté
    # 🧑‍🔧 Accessible depuis le dashboard contractor
    path(
        "my-bids/",
        my_bids_view,
        name="my-bids"
    ),

    # 🔹 Accepter une proposition
    path("accept/<int:bid_id>/", accept_bid_view, name="accept-bid"),

    # 🔹 Page temporaire de confirmation après acceptation
    path("accepted/confirmation/", bid_accepted_confirmation, name="bid-accepted-confirmation"),

]
