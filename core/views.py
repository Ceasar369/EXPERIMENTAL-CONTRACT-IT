# 📁 Fichier : core/views.py
# 🎯 Ce fichier contient toutes les vues publiques de l’application `core`.
# Chaque vue correspond à une page statique ou semi-dynamique visible par tous les utilisateurs :
#    - page d’accueil (index)
#    - pages d’information (how-to-hire, about, help, etc.)
#
# 👉 Ces vues sont appelées via les routes définies dans `core/urls.py`.
# 👉 Elles utilisent `render()` pour retourner un fichier HTML à afficher dans le navigateur.
# 👉 Aucune logique d’authentification, de JWT ou de sessions complexes ici.
# 👉 Toutes les pages utilisent des templates HTML situés dans : `core/templates/core/` ou ses sous-dossiers.

# ---------------------------------------------------------------------
# 📦 IMPORTS DJANGO
# ---------------------------------------------------------------------
from django.shortcuts import render  # 🧱 Fonction native pour afficher un template HTML
# ❌ Pas besoin ici de login, authenticate ou redirect — ce n’est pas une app d’authentification

# ---------------------------------------------------------------------
# 🌐 PAGE D’ACCUEIL — INDEX
# ---------------------------------------------------------------------
def index_view(request):
    """
    Affiche la page d’accueil publique de CONTRACT-IT.
    C’est la page principale visible en accédant à `/`.
    Elle peut contenir : section hero, témoignages, CTA, boutons d’inscription.
    """
    return render(request, 'core/index.html')

# ---------------------------------------------------------------------
# 🧑‍💼 PAGE : COMMENT EMBAUCHER UN ENTREPRENEUR
# ---------------------------------------------------------------------
def how_to_hire_view(request):
    """
    Page explicative à destination des clients.
    Contenu : comment fonctionne l'embauche sur la plateforme, les étapes, la sécurité.
    """
    return render(request, 'core/in_footer/how_to_hire.html')

# ---------------------------------------------------------------------
# 🧑‍🔧 PAGE : TROUVER DES TALENTS
# ---------------------------------------------------------------------
def talent_marketplace_view(request):
    """
    Page affichant les talents disponibles (ou leur catégorie).
    Elle pourra plus tard contenir une recherche ou un filtrage dynamique.
    """
    return render(request, 'core/in_footer/talent_marketplace.html')

# ---------------------------------------------------------------------
# 📦 PAGE : CATALOGUE DE PROJETS
# ---------------------------------------------------------------------
def project_catalog_view(request):
    """
    Page listant des exemples de projets réalisés.
    Objectif : inspirer les clients et leur montrer le type de services proposés.
    """
    return render(request, 'core/in_footer/project_catalog.html')

# ---------------------------------------------------------------------
# 👷 PAGE : COMMENT TROUVER DU TRAVAIL (POUR ENTREPRENEURS)
# ---------------------------------------------------------------------
def how_to_find_work_view(request):
    """
    Guide destiné aux entrepreneurs pour les aider à bien utiliser la plateforme :
    - comment postuler
    - comment se démarquer
    - comment gérer les jalons
    """
    return render(request, 'core/in_footer/how_to_find_work.html')

# ---------------------------------------------------------------------
# 🆘 PAGE : AIDE / CENTRE DE SUPPORT
# ---------------------------------------------------------------------
def help_support_view(request):
    """
    Page centrale regroupant les questions fréquentes (FAQ) et informations générales.
    Peut être enrichie plus tard avec une base de connaissances dynamique.
    """
    return render(request, 'core/in_footer/help.html')

# ---------------------------------------------------------------------
# ✉️ PAGE : CONTACTEZ-NOUS
# ---------------------------------------------------------------------
def contact_view(request):
    """
    Page avec les coordonnées de contact ou formulaire simple de message.
    Peut inclure : adresse email, lien vers support, formulaire de contact plus tard.
    """
    return render(request, 'core/in_footer/contact.html')

# ---------------------------------------------------------------------
# 🔒 PAGE : CONFIANCE ET SÉCURITÉ
# ---------------------------------------------------------------------
def trust_safety_view(request):
    """
    Page expliquant les mesures de sécurité de CONTRACT-IT.
    Elle rassure les utilisateurs (clients et entrepreneurs) sur la confidentialité et la modération.
    """
    return render(request, 'core/in_footer/trust_safety.html')

# ---------------------------------------------------------------------
# 🏢 PAGE : À PROPOS
# ---------------------------------------------------------------------
def about_view(request):
    """
    Page de présentation de la plateforme, de l'équipe, ou de la mission de l’entreprise.
    Texte marketing + crédibilité.
    """
    return render(request, 'core/in_footer/about.html')

# ---------------------------------------------------------------------
# ⚖️ PAGE : CONDITIONS D’UTILISATION
# ---------------------------------------------------------------------
def terms_view(request):
    """
    Conditions générales d’utilisation de la plateforme.
    Obligatoire pour la conformité juridique.
    """
    return render(request, 'core/in_footer/terms.html')

# ---------------------------------------------------------------------
# 🔐 PAGE : POLITIQUE DE CONFIDENTIALITÉ
# ---------------------------------------------------------------------
def privacy_view(request):
    """
    Politique expliquant comment les données personnelles sont traitées et protégées.
    Obligatoire pour être conforme au RGPD / Loi 25 (Québec).
    """
    return render(request, 'core/in_footer/privacy.html')

# ---------------------------------------------------------------------
# 🍪 PAGE : COOKIES
# ---------------------------------------------------------------------
def cookies_view(request):
    """
    Page expliquant le fonctionnement des cookies sur le site.
    Peut inclure la gestion du consentement ou les cookies tiers.
    """
    return render(request, 'core/in_footer/cookies.html')

# ---------------------------------------------------------------------
# 🧏 PAGE : ACCESSIBILITÉ
# ---------------------------------------------------------------------
def accessibility_view(request):
    """
    Page expliquant l’engagement de CONTRACT-IT pour l’accessibilité du site.
    Exemples : compatibilité lecteurs d’écran, navigation clavier, contraste.
    """
    return render(request, 'core/in_footer/accessibility.html')

# ---------------------------------------------------------------------
# 🌍 REDIRECTION AUTOMATIQUE VERS LA LANGUE PAR DÉFAUT
# ---------------------------------------------------------------------
from django.http import HttpResponseRedirect
from django.utils.translation import get_language

def redirect_to_language_home_view(request):
    """
    Redirige automatiquement l’utilisateur vers la langue courante détectée par Django.

    ➤ Exemple :
        - Si la langue par défaut est le français → redirige vers `/fr/`
        - Si l’utilisateur a sélectionné l’anglais → redirige vers `/en/`

    Cette vue est utilisée à la racine `/` pour éviter une erreur 404
    et orienter vers la bonne version localisée du site.
    """
    language = get_language() or "fr"  # Par défaut : français
    return HttpResponseRedirect(f"/{language}/")
