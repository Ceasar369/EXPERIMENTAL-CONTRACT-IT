# 📁 Fichier : accounts/models.py
# 🧠 Ce fichier définit les modèles de données utilisés pour représenter les utilisateurs sur la plateforme CONTRACT-IT.
# Il contient :
#   - le modèle `CustomUser`, qui remplace le modèle utilisateur standard de Django,
#   - ⚠️ les modèles `ExternalPortfolioItem` et `InternalPortfolioItem` sont annoncés mais pas encore définis.

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager  # ⚙️ Authentification personnalisée
from django.db import models                                # 📦 Définition des champs de modèle
from django.utils.translation import gettext_lazy as _      # 🌐 Pour la traduction des textes (français/anglais)

# ---------------------------------------------------------------------
# 🌍 Choix de langues possibles pour l’interface utilisateur
# ---------------------------------------------------------------------
LANGUAGE_CHOICES = (
    ('fr', _("Français")),
    ('en', _("Anglais")),
)

# ---------------------------------------------------------------------
# ⚙️ CustomUserManager : gestionnaire pour CustomUser sans champ username
# ---------------------------------------------------------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Crée un utilisateur standard à partir d'un email uniquement."""
        if not email:
            raise ValueError("L’adresse courriel doit être fournie.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # 🔐 Hachage du mot de passe
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Crée un superutilisateur avec tous les droits d'administration."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

# ---------------------------------------------------------------------
# 👤 Modèle principal : CustomUser
# Authentification par email, gestion multirôle (client + entrepreneur), 
# informations adaptées à chaque rôle CONTRACT-IT.
# ---------------------------------------------------------------------
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Modèle principal des utilisateurs CONTRACT-IT :
    - Remplace le modèle User par défaut
    - Supprime le champ `username` → l'email devient l’identifiant
    - Gère deux rôles : client et/ou entrepreneur
    - Supporte des champs spécifiques (portfolio, disponibilité, etc.)
    """

    # 📨 Identifiant principal
    email = models.EmailField(unique=True, help_text="Adresse courriel utilisée pour se connecter à la plateforme. Obligatoire.")

    # 🧍 Informations générales
    first_name = models.CharField(max_length=150, blank=True, help_text="Prénom de l'utilisateur. Optionnel.")
    last_name = models.CharField(max_length=150, blank=True, help_text="Nom de famille de l'utilisateur. Optionnel.")
    phone = models.CharField(max_length=15, blank=True, help_text="Numéro de téléphone. Optionnel.")
    city = models.CharField(max_length=100, help_text="Ville de résidence de l'utilisateur. Obligatoire.")
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='fr', help_text="Langue de l'interface utilisateur.")

    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        default='core/images/default-avatar.jpg',
        help_text="Photo de profil affichée publiquement. Optionnel."
    )
    bio = models.TextField(blank=True, help_text="Courte biographie affichée publiquement. Optionnel.")
    company_name = models.CharField(max_length=255, blank=True, help_text="Nom d'entreprise ou identité professionnelle. Optionnel.")
    is_verified = models.BooleanField(default=False, help_text="Statut de vérification validé manuellement par l'équipe. Optionnel.")
    date_joined = models.DateTimeField(auto_now_add=True, help_text="Date d'inscription de l'utilisateur. Générée automatiquement.")

    # 🏷️ Rôles utilisateurs
    is_client = models.BooleanField(default=False, help_text="L'utilisateur peut publier des projets (client).")
    is_contractor = models.BooleanField(default=False, help_text="L'utilisateur peut proposer ses services (entrepreneur).")

    # 🔧 Spécificités entrepreneur
    specialties = models.CharField(max_length=255, blank=True, help_text="Spécialités : plomberie, électricité, toiture, etc.")
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Tarif horaire proposé. Optionnel.")
    availability = models.CharField(max_length=100, blank=True, help_text="Disponibilité actuelle (ex. : Disponible en juin).")
    certifications = models.TextField(blank=True, help_text="Certifications détenues (RBQ, ASP, etc.).")

    # 📊 Statistiques client
    project_history_count = models.PositiveIntegerField(default=0, help_text="Nombre total de projets publiés.")

    # 🔐 Champs requis pour le fonctionnement du système
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['language']
    objects = CustomUserManager()

    is_active = models.BooleanField(default=True, help_text="Statut actif du compte.")
    is_staff = models.BooleanField(default=False, help_text="Autorisation d'accès à l’interface d’administration.")

    def __str__(self):
        """
        Affichage dans l'interface admin : prénom + nom ou email si vide.
        """
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.email

    def get_display_name(self):
        """
        Nom affiché publiquement (dans les profils, messages, etc.).
        """
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.email

    def is_profile_complete(self):
        """
        Vérifie si le profil contient les informations de base.
        Utile pour alerter ou bloquer certaines actions (soumission, réponse à projet…).
        """
        return all([
            self.first_name,
            self.last_name,
            self.city,
            self.profile_picture,
            self.is_verified
        ])
