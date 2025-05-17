# 📁 Fichier : core/urls.py
# 🧭 Ce fichier déclare toutes les routes (chemins d'URL) pour l'application `core`.
# Il fait le lien entre :
#     - l’URL demandée par l’utilisateur dans son navigateur (ex: /help/, /about/)
#     - la fonction Python correspondante dans views.py (ex: help_support, about)
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
from django.urls import path, include  # include est nécessaire pour relier l’app accounts
from . import views                    # 📥 On importe toutes les vues définies dans core/views.py

# ---------------------------------------------------------------------
# 🌐 DÉFINITION DES URLS
# ---------------------------------------------------------------------
urlpatterns = [

    # 🏠 Page d’accueil publique
    path('', views.index, name='index'),  # Ex: https://contract-it.ca/

    # -----------------------------------------------------------------
    # 📁 Pages destinées aux CLIENTS
    # -----------------------------------------------------------------
    path('how-to-hire/', views.how_to_hire, name='how_to_hire'),  # Guide pour clients
    path('talent-marketplace/', views.talent_marketplace, name='talent_marketplace'),  # Recherche de talents
    path('project-catalog/', views.project_catalog, name='project_catalog'),  # Exemples de projets

    # -----------------------------------------------------------------
    # 🧑‍🔧 Pages destinées aux ENTREPRENEURS
    # -----------------------------------------------------------------
    path('how-to-find-work/', views.how_to_find_work, name='how_to_find_work'),  # Guide pour entrepreneurs

    # -----------------------------------------------------------------
    # 🆘 Pages de support et d'information
    # -----------------------------------------------------------------
    path('help/', views.help_support, name='help'),            # Centre d’aide
    path('contact/', views.contact, name='contact'),           # Page de contact
    path('trust-safety/', views.trust_safety, name='trust_safety'),  # Sécurité et confiance

    # -----------------------------------------------------------------
    # 🏢 Pages "À propos" de l’entreprise
    # -----------------------------------------------------------------
    path('about/', views.about, name='about'),                 # À propos de Contract-IT
    path('terms/', views.terms, name='terms'),                 # Conditions d'utilisation
    path('privacy/', views.privacy, name='privacy'),           # Politique de confidentialité
    path('cookies/', views.cookies, name='cookies'),           # Politique de cookies
    path('accessibility/', views.accessibility, name='accessibility'),  # Accessibilité

    # -----------------------------------------------------------------
    # 🔐 Inclusion des routes de l’app `accounts` (gestion des utilisateurs)
    # -----------------------------------------------------------------
    # Cette ligne permet d'accéder aux vues liées à :
    # - login
    # - signup
    # - dashboard client / contractor
    # - et autres vues liées aux comptes
    path('accounts/', include('accounts.urls')),
]
