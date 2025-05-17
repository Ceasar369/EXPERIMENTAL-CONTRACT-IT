# 📁 Fichier : accounts/urls.py
# 🌐 Ce fichier définit les routes (URLs) accessibles pour les fonctionnalités liées aux comptes utilisateurs.
# Il est utilisé pour relier une URL à une vue Django classique (ex. : login, register, dashboard).
# Cette version est totalement indépendante de Django REST Framework et ne contient aucune API.
# Elle fonctionne uniquement avec les sessions Django, ce qui est parfait pour une application HTML classique.

# ---------------------------------------------------------------------
# 📦 IMPORTS NÉCESSAIRES
# ---------------------------------------------------------------------
from django.urls import path  # 🛤️ Permet de définir des chemins d’URL associés à des vues
from . import views           # 📥 On importe les vues HTML contenues dans accounts/views.py

# ---------------------------------------------------------------------
# 🔗 DÉFINITION DES URLS DISPONIBLES
# Chaque chemin ici est associé à une fonction dans views.py.
# Ces vues affichent des pages HTML ou effectuent des actions classiques (connexion, redirection...).
# ---------------------------------------------------------------------
urlpatterns = [

    # 🔐 Page de connexion
    # Affiche un formulaire de connexion (email + mot de passe) et connecte l'utilisateur.
    path("login/", views.login_view, name="login"),

    # 🆕 Page d'inscription
    # Affiche un formulaire d'inscription pour créer un compte client ou entrepreneur.
    path("register/", views.register_view, name="register"),

    # 💼 Tableau de bord HTML pour les clients
    # Accessible uniquement aux utilisateurs avec is_client=True.
    path("dashboard/client/", views.client_dashboard, name="client-dashboard"),

    # 👷 Tableau de bord HTML pour les entrepreneurs
    # Accessible uniquement aux utilisateurs avec is_contractor=True.
    path("dashboard/contractor/", views.contractor_dashboard, name="contractor-dashboard"),

    # 🚪 Déconnexion
    # Met fin à la session Django et redirige vers la page d’accueil ou de login.
    path("logout/", views.logout_view, name="logout"),

    # 👷 Profil public d’un entrepreneur 
    # 🔎 Vue publique d’un entrepreneur 
    path("contractors/<int:user_id>/", views.contractor_detail_view, name="contractor_detail"),

]
