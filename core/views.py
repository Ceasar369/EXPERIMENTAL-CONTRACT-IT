# core/views.py
from django.utils.translation import gettext as _
from django.shortcuts import render


def index(request):
    return render(request, 'core/index.html')  # Nouvelle landing publique

def how_to_hire(request):
    return render(request, 'core/in_footer/how_to_hire.html')  # Page explicative pour les clients : comment embaucher

def talent_marketplace(request):
    return render(request, 'core/in_footer/talent_marketplace.html')  # Présentation des talents disponibles

def project_catalog(request):
    return render(request, 'core/in_footer/project_catalog.html')  # Catalogue de projets ou d'exemples inspirants

def how_to_find_work(request):
    return render(request, 'core/in_footer/how_to_find_work.html')  # Aide pour les entrepreneurs : comment trouver du travail

def help_support(request):
    return render(request, 'core/in_footer/help.html')  # Centre d'aide ou FAQ

def contact(request):
    return render(request, 'core/in_footer/contact.html')  # Page de contact général (ou lien vers support)

def trust_safety(request):
    return render(request, 'core/in_footer/trust_safety.html')  # Règles de sécurité, politique de confiance

def about(request):
    return render(request, 'core/in_footer/about.html')  # Page "À propos" de la compagnie

def terms(request):
    return render(request, 'core/in_footer/terms.html')  # Conditions d'utilisation de la plateforme

def privacy(request):
    return render(request, 'core/in_footer/privacy.html')  # Politique de confidentialité

def cookies(request):
    return render(request, 'core/in_footer/cookies.html')  # Paramètres ou politique sur les cookies

def accessibility(request):
    return render(request, 'core/in_footer/accessibility.html')  # Accessibilité du site pour tous les utilisateurs

def signup(request):
    return render(request, 'core/signup.html')

def login_view(request):
    return render(request, 'core/login.html')

def contractor_dashboard(request):
    return render(request, 'core/contractor_dashboard.html')

def client_dashboard(request):
    return render(request, 'core/client_dashboard.html')

