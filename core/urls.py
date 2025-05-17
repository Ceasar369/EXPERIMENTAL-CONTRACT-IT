# 📁 Fichier : core/urls.py
# 🧭 Ce fichier déclare toutes les routes (chemins d'URL) pour l'application `core`.
# Il fait le lien entre :
#     - l’URL demandée par l’utilisateur dans son navigateur (ex: /help/, /about/)
#     - la fonction Python correspondante dans views.py (ex: help_support_view, about_view)
#
# 🧩 Ce fichier est utilisé pour les pages :
#     - publiques (index, help, contact…)
#     - neutres, accessibles à tous les rôles (client, entrepreneur ou visiteur)
#
# ❌ Aucune logique d’API, de JWT ou de REST ici — uniquement des vues HTML classiques.
# ❌ Les vues liées aux comptes utilisateurs (login, signup, dashboards) sont maintenant gérées exclusivement dans `accounts/`.

# ---------------------------------------------------------------------
# 📦 IMPORTS
# ---------------------------------------------------------------------
from django.urls import path, include                     # include permet de relier l’app accounts
from . import views                                       # 📥 Import des vues de core/views.py

# ---------------------------------------------------------------------
# 🌐 DÉFINITION DES URLS
# ---------------------------------------------------------------------
urlpatterns = [

    # 🏠 Page d’accueil publique
    path('', views.index_view, name='index_view'),

    # -----------------------------------------------------------------
    # 📁 Pages destinées aux CLIENTS
    # -----------------------------------------------------------------
    path('how_to_hire/', views.how_to_hire_view, name='how_to_hire_view'),                  # Guide pour clients
    path('talent_marketplace/', views.talent_marketplace_view, name='talent_marketplace_view'),  # Recherche de talents
    path('project_catalog/', views.project_catalog_view, name='project_catalog_view'),      # Exemples de projets

    # -----------------------------------------------------------------
    # 🧑‍🔧 Pages destinées aux ENTREPRENEURS
    # -----------------------------------------------------------------
    path('how_to_find_work/', views.how_to_find_work_view, name='how_to_find_work_view'),   # Guide pour entrepreneurs

    # -----------------------------------------------------------------
    # 🆘 Pages de support et d'information
    # -----------------------------------------------------------------
    path('help/', views.help_support_view, name='help_support_view'),                 # Centre d’aide
    path('contact/', views.contact_view, name='contact_view'),               # Page de contact
    path('trust_safety/', views.trust_safety_view, name='trust_safety_view'),# Sécurité et confiance

    # -----------------------------------------------------------------
    # 🏢 Pages "À propos" de l’entreprise
    # -----------------------------------------------------------------
    path('about/', views.about_view, name='about_view'),                     # À propos de Contract-IT
    path('terms/', views.terms_view, name='terms_view'),                     # Conditions d'utilisation
    path('privacy/', views.privacy_view, name='privacy_view'),              # Politique de confidentialité
    path('cookies/', views.cookies_view, name='cookies_view'),              # Politique de cookies
    path('accessibility/', views.accessibility_view, name='accessibility_view'),  # Accessibilité

    # -----------------------------------------------------------------
    # 🔐 Inclusion des routes de l’app `accounts` (gestion des utilisateurs)
    # -----------------------------------------------------------------
    path('accounts/', include('accounts.urls')),  # Vues liées à login, signup, dashboards, etc.
]
