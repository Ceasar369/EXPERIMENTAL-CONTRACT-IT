# 📁 Fichier : accounts/models.py
# 🧠 Ce fichier définit les modèles de données utilisés pour représenter les utilisateurs sur la plateforme CONTRACT-IT.
# Plus précisément, il contient :
#   - le modèle `CustomUser`, qui remplace le modèle utilisateur standard de Django,
#   - un modèle `ExternalPortfolioItem` pour les projets réalisés en dehors de la plateforme,
#   - un modèle `InternalPortfolioItem` pour les projets réalisés via CONTRACT-IT et liés à un projet publié.

# 🔁 Import des modules de base pour les modèles Django
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager  # ⚙️ Authentification personnalisée
from django.db import models                              # 📦 Outils pour définir des champs (CharField, BooleanField, etc.)
from django.forms import ValidationError                  # ⚠️ Utilisé pour ajouter une règle de validation personnalisée
from django.utils.translation import gettext_lazy as _    # 🌐 Pour rendre les textes traduisibles (multi-langues)

# ---------------------------------------------------------------------
# 🌍 Choix de langues possibles pour l’interface utilisateur
# On utilise une liste de tuples, chaque tuple = (valeur en base de données, label affiché)
# ---------------------------------------------------------------------
LANGUAGE_CHOICES = (
    ('fr', _("Français")),  # Choix 1 : Français
    ('en', _("Anglais")),   # Choix 2 : Anglais
)

# ---------------------------------------------------------------------
# ⚙️ CustomUserManager : gestionnaire d'utilisateurs sans username
# Utilisé pour créer des utilisateurs avec uniquement l'email comme identifiant.
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
# Il remplace le modèle User de Django en y ajoutant des champs adaptés à CONTRACT-IT.
# Chaque utilisateur peut être un client, un entrepreneur, ou les deux.
# ---------------------------------------------------------------------
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Ce modèle hérite de AbstractBaseUser (au lieu de AbstractUser), ce qui :
    - supprime totalement le champ `username`
    - nous oblige à gérer les permissions avec PermissionsMixin
    - permet d'utiliser l'email comme identifiant principal

    ➤ Il supprime le champ `username`
    ➤ Utilise `email` comme identifiant de connexion
    ➤ Contient des champs supplémentaires pour les rôles CONTRACT-IT
    """

    # ✅ On utilise l’email comme champ de connexion
    email = models.EmailField(unique=True, help_text="Adresse courriel utilisée pour se connecter à la plateforme.")

    # ✅ Champs de nom à ajouter explicitement, car on a supprimé `username`
    first_name = models.CharField(max_length=150, blank=True, help_text="Prénom de l'utilisateur (optionnel).")
    last_name = models.CharField(max_length=150, blank=True, help_text="Nom de famille de l'utilisateur (optionnel).")


    # ----------------------------- Champs communs -----------------------------
    phone = models.CharField(max_length=15, blank=True, help_text="Numéro de téléphone de l'utilisateur.")
    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        default='core/images/default-avatar.jpg',  # 📌 Chemin relatif dans static/
        help_text="Photo de profil affichée dans le profil public."
    )
    bio = models.TextField(blank=True, help_text="Courte biographie affichée dans le profil public.")
    city = models.CharField(max_length=100, help_text="Ville de résidence de l'utilisateur.")
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='fr', help_text="Langue de l'interface utilisateur (français ou anglais).")
    is_verified = models.BooleanField(default=False, help_text="Statut de vérification manuel par l'équipe CONTRACT-IT.")
    date_joined = models.DateTimeField(auto_now_add=True, help_text="Date d'inscription de l'utilisateur.")
    company_name = models.CharField(max_length=255, blank=True, help_text="Nom de l'entreprise ou identité professionnelle (optionnel).")

    # ----------------------------- Champs de rôle -----------------------------
    is_client = models.BooleanField(default=False, help_text="Définit si l'utilisateur peut publier des projets (client).")
    is_contractor = models.BooleanField(default=False, help_text="Définit si l'utilisateur peut proposer ses services (entrepreneur).")

    # ---------------------- Champs spécifiques aux entrepreneurs ----------------------
    specialties = models.CharField(max_length=255, blank=True, help_text="Spécialités professionnelles : plomberie, électricité, toiture, etc.")
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Tarif horaire proposé par l'entrepreneur (optionnel).")
    availability = models.CharField(max_length=100, blank=True, help_text="Disponibilité actuelle (ex. : Disponible en juin).")
    certifications = models.TextField(blank=True, help_text="Certifications détenues (ex. RBQ, ASP, etc.).")

    # ---------------------- Champs spécifiques aux clients ----------------------
    project_history_count = models.PositiveIntegerField(default=0, help_text="Nombre total de projets publiés par ce client.")

    # ✅ Obligatoire pour AbstractBaseUser → on indique le champ qui sert d’identifiant
    USERNAME_FIELD = 'email'
    # ✅ Champs requis uniquement pour les superutilisateurs (ex. : via createsuperuser)
    REQUIRED_FIELDS = ['language']

    # ✅ Manager personnalisé
    objects = CustomUserManager()

    # ✅ Obligatoire pour que Django reconnaisse ce modèle comme utilisateur
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        """
        Affichage dans l'admin : prénom + nom si disponibles, sinon email.
        """
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.email

    def get_display_name(self):
        """
        Nom complet à afficher publiquement sur la plateforme (ex : profil public).
        Peut être modifié plus tard pour intégrer un nom d’usage ou un slug.
        """
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.email


