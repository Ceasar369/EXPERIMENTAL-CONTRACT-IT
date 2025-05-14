# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

LANGUAGE_CHOICES = (
    ('fr', _("Français")),
    ('en', _("Anglais")),
)

# ------------------------------------------------------------------------------
# 👤 Modèle utilisateur personnalisé utilisé pour tous les utilisateurs CONTRACT-IT
# Hérite de AbstractUser pour bénéficier du système d’authentification Django
# ------------------------------------------------------------------------------
class CustomUser(AbstractUser):
    # 🎯 Champs communs pour tous les types d’utilisateurs (clients et entrepreneurs)
    email = models.EmailField(unique=True, help_text="Adresse courriel pour se connecter et recevoir les notifications")
    phone = models.CharField(max_length=15, blank=True, help_text="Numéro de téléphone de l'utilisateur")
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, help_text="Photo de profil affichée publiquement")
    bio = models.TextField(blank=True, help_text="Brève biographie affichée sur le profil")
    city = models.CharField(max_length=100, blank=True, help_text="Ville de résidence de l'utilisateur")
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='fr', help_text=_("Langue d'affichage de l'interface"))
    is_verified = models.BooleanField(default=False, help_text="Indique si l'utilisateur est vérifié par l'équipe admin")
    date_joined = models.DateTimeField(auto_now_add=True, help_text="Date d'inscription sur la plateforme")
    company_name = models.CharField(max_length=255, blank=True, help_text="Nom de l'entreprise") # ℹ️ Le champ "company_name" est utile pour afficher une identité professionnelle même pour des travailleurs autonomes.


    # ✅ Champs de rôle (au moins un sera True selon le type d’utilisateur)
    is_client = models.BooleanField(default=False, help_text="Définit si l'utilisateur est un client")
    is_contractor = models.BooleanField(default=False, help_text="Définit si l'utilisateur est un entrepreneur")

    # 👷‍♂️ Champs spécifiques aux entrepreneurs (affichés sur leur profil public)
    specialties = models.CharField(max_length=255, blank=True, help_text="Domaines de spécialité : ex. Plomberie, Électricité")
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Tarif horaire affiché publiquement")
    availability = models.CharField(max_length=100, blank=True, help_text="Disponibilité générale : ex. Disponible dès juin")
    certifications = models.TextField(blank=True, help_text="Certifications professionnelles (ex. RBQ, ASP, etc.)")

    # 👤 Champs spécifiques aux clients (non obligatoires mais utiles pour enrichir leur profil)
    project_history_count = models.PositiveIntegerField(default=0, help_text="Nombre total de projets publiés par le client")

    # 🔁 Affichage dans l’admin ou debug
    def __str__(self):
        return self.username


# ------------------------------------------------------------------------------
# 📁 Modèle PortfolioItem : représente une réalisation d’un utilisateur (surtout entrepreneur)
# Peut être liée à un projet réalisé sur CONTRACT-IT, ou être une réalisation externe
# ------------------------------------------------------------------------------



# -------------------------------------------------------------------------------
# 📁 Projet EXTERNE – Portfolio manuel ajouté par l'entrepreneur
# -------------------------------------------------------------------------------
class ExternalPortfolioItem(models.Model):
      #  Lien avec l'utilisateur qui publie cette réalisation (généralement un entrepreneur)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='external_portfolio_items',
        help_text="Utilisateur ayant réalisé ce projet externe"
    )

        #  Titre et description du projet

    title = models.CharField(max_length=100, help_text="Titre du projet externe")

    description = models.TextField(blank=True, help_text="Description du projet")
        #  Image illustrative du projet (facultative)
    image = models.ImageField(upload_to='portfolio/external/', blank=True, null=True)

     #  Date de publication du portfolio sur CONTRACT-IT (non liée à la date de réalisation réelle)
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date d'ajout dans le portfolio")

    def __str__(self):
        return f"[EXTERNE] {self.title} - {self.user.username}"



# -------------------------------------------------------------------------------
# 📁 Projet INTERNE – Réalisé via CONTRACT-IT, relié à un vrai modèle Project
# Ce modèle représente une réalisation liée à un projet effectué sur la plateforme.
# Chaque réalisation correspond à UN SEUL projet (relation OneToOne).
# -------------------------------------------------------------------------------
class InternalPortfolioItem(models.Model):

    # 👤 Utilisateur (entrepreneur) qui a réalisé ce projet
    user = models.ForeignKey(
        CustomUser,  # Modèle utilisateur personnalisé (souvent is_contractor = True)
        on_delete=models.CASCADE,  # Si l'utilisateur est supprimé, on supprime aussi son portfolio
        related_name='internal_portfolio_items',  # Permet d’accéder aux items via user.internal_portfolio_items.all()
        help_text="Utilisateur ayant réalisé ce projet CONTRACT-IT"
    )

    # 🔗 Projet CONTRACT-IT associé à cette réalisation (relation 1:1)
    project = models.OneToOneField(
        'projects.Project',  # Référence différée pour éviter les imports circulaires
        on_delete=models.CASCADE,  # Si le projet est supprimé, le portfolio l'est aussi
        related_name='internal_portfolio_item',  # Permet d’accéder à l’item via project.internal_portfolio_item
        help_text="Projet réalisé via CONTRACT-IT (doit exister dans la plateforme)"
    )

    # 📝 Notes complémentaires laissées par l’entrepreneur (résultats, résumé, commentaires)
    notes = models.TextField(
        blank=True,  # facultatif
        help_text="Commentaires ou résultats du projet"
    )

    # 🕒 Date d’ajout de cette réalisation au portfolio interne
    created_at = models.DateTimeField(
        auto_now_add=True  # prend la date au moment de la création
    )

    # ✅ Validation logique personnalisée : vérifie que l'entrepreneur est bien le contractor du projet lié
    def clean(self):
        if self.project.contractor != self.user:
            raise ValidationError("Ce projet n'a pas été réalisé par cet utilisateur.")  # empêche les erreurs de liaison

    # 🔁 Affichage lisible dans l’interface admin ou dans les logs
    def __str__(self):
        return f"[CONTRACT-IT] {self.project.title} - {self.user.username}"
