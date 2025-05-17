# 📁 Fichier : accounts/urls.py
# 🌐 Ce fichier définit les routes HTML accessibles pour les comptes utilisateurs CONTRACT-IT.
# Ces vues fonctionnent avec les sessions Django classiques (pas de DRF ici).
# Chaque chemin est associé à une vue déclarée dans accounts/views.py.

# ---------------------------------------------------------------------
# 📦 IMPORTS
# ---------------------------------------------------------------------
from django.urls import path                # 🛤️ Outil de routage Django
from . import views                         # 📥 Import des vues HTML

# ---------------------------------------------------------------------
# 🔗 DÉFINITION DES ROUTES DISPONIBLES
# ---------------------------------------------------------------------
urlpatterns = [

    # ------------------------
    # 🔐 Authentification
    # ------------------------

    path("login/", views.login_view, name="login_view"),                         # Formulaire de connexion
    path("register/", views.register_view, name="register_view"),               # Formulaire d'inscription
    path("logout/", views.logout_view, name="logout_view"),                     # Déconnexion utilisateur

    # ------------------------
    # 📊 Dashboards utilisateurs
    # ------------------------

    path("dashboard/client/", views.client_dashboard_view, name="client_dashboard_view"),           # Tableau de bord client
    path("dashboard/contractor/", views.contractor_dashboard_view, name="contractor_dashboard_view"),  # Tableau de bord entrepreneur

    # ------------------------
    # 👷 Vue publique des utilisateurs
    # ------------------------

    path("clients/<int:user_id>/", views.client_detail_view, name="client_detail_view"),       # Profil public d’un client
    path("contractors/<int:user_id>/", views.contractor_detail_view, name="contractor_detail_view"),  # Profil public d’un entrepreneur

]
