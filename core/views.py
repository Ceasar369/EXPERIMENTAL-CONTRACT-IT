# core/views.py
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from accounts.models import CustomUser  # 🔁 Pour recharger l'utilisateur avec is_client/is_contractor


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
    # 👤 Si l'utilisateur soumet le formulaire (méthode POST)
    if request.method == "POST":
        # 🔐 Récupère les données du formulaire
        username = request.POST.get("username")
        password = request.POST.get("password")

        # 🔍 Authentifie l'utilisateur (renvoie None si mauvais identifiants)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # ✅ Recharge l'objet CustomUser avec tous les champs (is_client, is_contractor, etc.)
            user = CustomUser.objects.get(pk=user.pk)

            # 🔐 Connecte l'utilisateur via session Django
            login(request, user)

            # 🎯 Redirige automatiquement selon le rôle
            if user.is_client:
                return redirect('/dashboard/client/')
            elif user.is_contractor:
                return redirect('/dashboard/contractor/')
            else:
                return redirect('/')  # Fallback si pas de rôle (admin ?)

        else:
            # ❌ Si l'authentification échoue, on affiche une erreur
            return render(request, 'core/login.html', {
                'error': "Identifiants invalides. Veuillez réessayer."
            })

    # 👁️ Affiche simplement le formulaire si GET
    return render(request, 'core/login.html')

# 💼 Dashboard HTML pour les entrepreneurs (non-API)
def contractor_dashboard(request):
    return render(request, 'core/contractor_dashboard.html', {
        'user': request.user  # ✅ Passe l'objet CustomUser au template
    })

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from projects.models import Project
from bids.models import Bid

# ✅ Dashboard HTML pour client
@login_required
def client_dashboard(request):
    user = request.user

    # 🔍 Récupère les projets publiés par le client
    projects = Project.objects.filter(client=user)

    # 🧮 Prépare la liste avec le nombre de bids
    project_data = []
    for project in projects:
        bids_count = Bid.objects.filter(project=project).count()
        project_data.append({
            'project': project,
            'bids_count': bids_count,
        })

    return render(request, 'core/client_dashboard.html', {
        'projects_with_bids': project_data
    })


