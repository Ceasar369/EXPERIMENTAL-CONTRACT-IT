# 📁 Fichier : accounts/views.py
# 🌐 Ce fichier contient toutes les vues HTML classiques pour gérer les comptes utilisateurs dans CONTRACT-IT.
# Il s’agit notamment des pages suivantes :
#   - Connexion (`login_view`)
#   - Inscription (`register_view`)
#   - Déconnexion (`logout_view`)
#   - Dashboard client (`client_dashboard_view`)
#   - Dashboard entrepreneur (`contractor_dashboard_view`)
#   - Vue publique d’un entrepreneur (`contractor_detail_view`)
# Toutes ces vues utilisent les sessions Django classiques et ne nécessitent pas de token ou d’API.

# ---------------------------------------------------------------------
# 📦 IMPORTS ESSENTIELS
# ---------------------------------------------------------------------
from decimal import Decimal, InvalidOperation              # 🔢 Conversion sécurisée du tarif horaire
from django.shortcuts import render, redirect              # 🔁 Affichage de templates ou redirections
from django.contrib.auth import authenticate, login, logout  # 🔐 Authentification Django
from django.contrib.auth.decorators import login_required  # ✅ Restriction d’accès
from django.http import Http404                            # ❌ Pour lever une erreur 404
from .models import CustomUser                             # 👤 Modèle utilisateur personnalisé
from .permissions import client_required, contractor_required  # 🔒 Décorateurs personnalisés

# ---------------------------------------------------------------------
# 🔐 Page de connexion — login_view
# ---------------------------------------------------------------------
def login_view(request):
    """
    Affiche le formulaire de connexion (email + mot de passe) et valide les identifiants.
    Redirige automatiquement vers le bon dashboard selon le rôle de l’utilisateur.
    """
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            # 🔁 Redirection automatique selon le rôle principal
            if user.is_client and not user.is_contractor:
                return redirect("client_dashboard_view")  # ✅ Nouveau nom avec underscore
            elif user.is_contractor and not user.is_client:
                return redirect("contractor_dashboard_view")  # ✅ Nouveau nom avec underscore
            else:
                # 👥 Cas hybride → redirection client par défaut (modifiable)
                return redirect("client_dashboard_view")  # ✅ Nouveau nom avec underscore
        else:
            return render(request, "accounts/login.html", {
                "error": "Adresse courriel ou mot de passe incorrect."
            })

    return render(request, "accounts/login.html")

# ---------------------------------------------------------------------
# 🆕 Page d’inscription — register_view
# ---------------------------------------------------------------------
def register_view(request):
    """
    Affiche un formulaire d'inscription et enregistre un nouvel utilisateur avec son rôle.
    Associe un ou deux rôles (client, entrepreneur) dès l'inscription.
    """
    if request.method == "POST":
        email = request.POST.get("email")
        if CustomUser.objects.filter(email=email).exists():
            return render(request, "accounts/register.html", {
                "error": "Un compte avec cette adresse existe déjà. Veuillez vous connecter."
            })

        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone = request.POST.get("phone")
        city = request.POST.get("city")

        is_client = bool(request.POST.get("is_client"))
        is_contractor = bool(request.POST.get("is_contractor"))

        # 🛑 Vérification qu'au moins un rôle est sélectionné
        if not is_client and not is_contractor:
            return render(request, "accounts/register.html", {
                "error": "Vous devez choisir au moins un rôle (client ou entrepreneur)."
            })

        specialties = request.POST.get("specialties", "")
        company_name = request.POST.get("company_name", "")
        certifications = request.POST.get("certifications", "")
        availability = request.POST.get("availability", "")

        hourly_rate_raw = request.POST.get("hourly_rate")
        try:
            hourly_rate = Decimal(hourly_rate_raw) if hourly_rate_raw else None
        except (InvalidOperation, TypeError):
            hourly_rate = None

        # ✅ Création de l'utilisateur (l'image de profil par défaut est gérée par le modèle)
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
            availability=availability
        )

        login(request, user)

        if is_client and not is_contractor:
            return redirect("client_dashboard_view")  # ✅ Nouveau nom avec underscore
        elif is_contractor and not is_client:
            return redirect("contractor_dashboard_view")  # ✅ Nouveau nom avec underscore
        else:
            return redirect("client_dashboard_view")  # ✅ Nouveau nom avec underscore

    return render(request, "accounts/register.html")

# ---------------------------------------------------------------------
# 🚪 Déconnexion — logout_view
# ---------------------------------------------------------------------
def logout_view(request):
    """
    Déconnecte l’utilisateur et redirige vers la page d’accueil.
    """
    logout(request)
    return redirect("/")

# ---------------------------------------------------------------------
# 🧑‍💼 Tableau de bord client — client_dashboard_view
# ---------------------------------------------------------------------
@login_required
@client_required
def client_dashboard_view(request):
    """
    Vue principale pour les utilisateurs avec le rôle client.
    Affiche leurs projets, messages, paiements, etc.
    """
    return render(request, "accounts/client_dashboard.html", {
        "user": request.user
    })

# ---------------------------------------------------------------------
# 👷 Tableau de bord entrepreneur — contractor_dashboard_view
# ---------------------------------------------------------------------
@login_required
@contractor_required
def contractor_dashboard_view(request):
    """
    Vue principale pour les utilisateurs avec le rôle entrepreneur.
    Affiche les projets disponibles, mandats en cours, outils de gestion.
    """
    return render(request, "accounts/contractor_dashboard.html", {
        "user": request.user
    })

# ---------------------------------------------------------------------
# 🧾 Vue publique d’un client — client_detail_view
# ---------------------------------------------------------------------
def client_detail_view(request, user_id):
    """
    Affiche le profil public d’un client CONTRACT-IT.
    Vérifie que l’utilisateur demandé est bien un client (is_client = True).

    🔗 Accessible depuis une page de projet ou de recherche.

    📌 Ce profil inclut :
        - Informations générales (nom, ville, bio…)
        - Statut de vérification
        - Nombre de projets publiés
    """
    try:
        profile = CustomUser.objects.get(id=user_id, is_client=True)
    except CustomUser.DoesNotExist:
        raise Http404("Ce client n'existe pas ou n'est pas visible publiquement.")

    return render(request, "accounts/client_detail.html", {
        "profile": profile
    })


# ---------------------------------------------------------------------
# 🧾 Vue publique d’un entrepreneur — contractor_detail_view
# ---------------------------------------------------------------------
def contractor_detail_view(request, user_id):
    """
    Affiche le profil public d’un entrepreneur (accessible depuis la recherche).
    Vérifie que l’utilisateur est bien un entrepreneur.
    """
    try:
        profile = CustomUser.objects.get(id=user_id, is_contractor=True)
    except CustomUser.DoesNotExist:
        raise Http404("Cet entrepreneur n'existe pas ou n'est pas visible publiquement.")

    # ✅ Vérifie s’il existe des projets externes
    external_has = profile.external_portfolio_items.exists()

    # ✅ Prépare la liste des projets internes visibles
    internal_visible_items = profile.internal_portfolio_items.filter(visible_in_portfolio=True)

    # ✅ Vérifie s’il existe des projets internes visibles
    internal_has = internal_visible_items.exists()

    return render(request, "accounts/contractor_detail.html", {
        "profile": profile,
        "external_has": external_has,
        "internal_visible_items": internal_visible_items,
        "internal_has": internal_has,
    })

