# 📁 Fichier : accounts/views.py
# 🌐 Ce fichier contient toutes les vues HTML classiques pour gérer les comptes utilisateurs dans CONTRACT-IT.
# Il s’agit notamment des pages suivantes :
#   - Connexion (`login_view`)
#   - Inscription (`register_view`)
#   - Déconnexion (`logout_view`)
#   - Dashboard client
#   - Dashboard entrepreneur
# Toutes ces vues utilisent les sessions Django classiques et ne nécessitent pas de token ou d’API.

# ---------------------------------------------------------------------
# 📦 IMPORTS ESSENTIELS
# ---------------------------------------------------------------------
from django.shortcuts import render, redirect         # 🔁 Pour afficher des templates ou rediriger l’utilisateur
from django.contrib.auth import authenticate, login, logout  # 🔐 Fonctions de gestion de l’authentification
from django.contrib.auth.decorators import login_required     # ✅ Pour restreindre l’accès aux utilisateurs connectés
from django.contrib import messages  # ✅ Pour afficher un message d’erreur dans le template
from .models import CustomUser                        # 👤 Modèle utilisateur personnalisé
from .permissions import client_required, contractor_required  # 🔒 Décorateurs personnalisés définis dans permissions.py

# ---------------------------------------------------------------------
# 🔐 Page de connexion — login_view
# Cette vue affiche un formulaire de connexion (email + mot de passe).
# Si les identifiants sont valides, elle redirige l’utilisateur vers le bon dashboard selon son rôle.
# ---------------------------------------------------------------------
def login_view(request):
    """
    Cette vue gère l’affichage du formulaire de connexion et la validation des identifiants.
    Elle redirige automatiquement vers le bon dashboard selon le rôle de l’utilisateur.
    """
    if request.method == "POST":
        # 🔄 Récupération des données du formulaire
        email = request.POST.get("email")
        password = request.POST.get("password")

        # 🔐 Tentative de connexion avec les identifiants
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # ✅ Connexion réussie → on démarre la session
            login(request, user)

            # 🔁 Redirection automatique selon le rôle
            if user.is_client and not user.is_contractor:
                return redirect("client-dashboard")
            elif user.is_contractor and not user.is_client:
                return redirect("contractor-dashboard")
            else:
                # 🎯 Cas spécial : utilisateur hybride → on choisit un dashboard par défaut
                return redirect("client-dashboard")  # (ou contractor-dashboard si tu préfères)
        else:
            # ❌ Identifiants incorrects → message d’erreur
            return render(request, "accounts/login.html", {
                "error": "Adresse courriel ou mot de passe incorrect."
            })

    # 🖼️ Affichage initial du formulaire
    return render(request, "accounts/login.html")

# ---------------------------------------------------------------------
# 🆕 Page d’inscription — register_view
# Permet de créer un nouveau compte utilisateur avec un rôle (client ou entrepreneur ou les deux).
# ---------------------------------------------------------------------
def register_view(request):
    """
    Affiche un formulaire d'inscription et enregistre un nouvel utilisateur dans la base.
    Permet de définir le rôle dès l’inscription (client, entrepreneur, ou les deux).
    """
    if request.method == "POST":
        email = request.POST.get("email")
        if CustomUser.objects.filter(email=email).exists():
            # 🚫 Email déjà utilisé → on renvoie une erreur à l’utilisateur
            return render(request, "accounts/register.html", {
                "error": _("An account with this email already exists. Please log in instead.")
            })

        # 🔄 On récupère les autres champs
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone = request.POST.get("phone")
        city = request.POST.get("city")
        is_client = bool(request.POST.get("is_client"))
        is_contractor = bool(request.POST.get("is_contractor"))
        specialties = request.POST.get("specialties", "")
        company_name = request.POST.get("company_name", "")
        certifications = request.POST.get("certifications", "")
        hourly_rate = request.POST.get("hourly_rate") or None
        availability = request.POST.get("availability", "")

        # ✅ Création avec image par défaut
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            city=city,
            is_client=is_client,
            is_contractor=is_contractor,
            specialties=specialties,
            company_name=company_name,
            certifications=certifications,
            hourly_rate=hourly_rate,
            availability=availability,
            profile_picture="core/images/default-avatar.jpg"  # ✅ image par défaut
        )

        # 🔐 Connexion automatique après inscription
        login(request, user)

        # 🔁 Redirection vers le bon dashboard
        if is_client and not is_contractor:
            return redirect("client-dashboard")
        elif is_contractor and not is_client:
            return redirect("contractor-dashboard")
        else:
            return redirect("client-dashboard")  # utilisateur hybride → dashboard client par défaut

    # 🖼️ Affichage du formulaire d’inscription
    return render(request, "accounts/register.html")

# ---------------------------------------------------------------------
# 🚪 Déconnexion — logout_view
# Termine la session Django et redirige vers la page d’accueil.
# ---------------------------------------------------------------------
def logout_view(request):
    """
    Ferme la session de l’utilisateur (logout) et redirige vers la page d’accueil.
    """
    logout(request)              # 🔐 Met fin à la session de l'utilisateur connecté
    return redirect("/")         # 🔁 Redirection vers la racine du site (peut être /login si tu préfères)

# ---------------------------------------------------------------------
# 🧑‍💼 Dashboard client — client_dashboard
# Accessible uniquement aux utilisateurs ayant le rôle client (is_client = True)
# ---------------------------------------------------------------------
@login_required                 # ✅ L’utilisateur doit être connecté
@client_required               # 🔒 Il doit être un client
def client_dashboard(request):
    """
    Cette vue affiche le tableau de bord du client.
    Elle peut contenir la liste des projets publiés, les propositions reçues, etc.
    """
    return render(request, "accounts/client_dashboard.html", {
        "user": request.user
    })

# ---------------------------------------------------------------------
# 👷 Dashboard entrepreneur — contractor_dashboard
# Accessible uniquement aux utilisateurs ayant le rôle entrepreneur (is_contractor = True)
# ---------------------------------------------------------------------
@login_required                 # ✅ L’utilisateur doit être connecté
@contractor_required           # 🔒 Il doit être un entrepreneur
def contractor_dashboard(request):
    """
    Cette vue affiche le tableau de bord de l’entrepreneur.
    Elle peut contenir les projets disponibles à soumissionner, les projets en cours, etc.
    """
    return render(request, "accounts/contractor_dashboard.html", {
        "user": request.user
    })
