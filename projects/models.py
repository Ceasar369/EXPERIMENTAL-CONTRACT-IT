# ---------------------------------------------------------------------
# 📁 Fichier : projects/models.py
#
# 🏗️ Modèles liés aux projets CONTRACT-IT
#
# Ce fichier contient deux classes de modèles :
#
# 1. 🔹 `Project` :
#    Représente un projet publié par un client (ex : rénovation salle de bain).
#    Contient toutes les informations nécessaires à sa création, sa gestion
#    et son suivi : client, entrepreneur, budget, deadline, statut, etc.
#
# 2. 🔹 `Milestone` :
#    Représente une étape (jalon) dans un projet.
#    Chaque jalon correspond à une tâche spécifique (ex : démolition, carrelage),
#    avec son propre budget, échéance et statut de validation.
#    Le paiement d’un projet peut être conditionné à l’approbation de ses jalons.
#
# Ces deux modèles sont utilisés :
#    - dans l’interface admin,
#    - dans les vues HTML classiques (liste, création, détail),
#    - plus tard, dans les APIs REST si activées.
# ---------------------------------------------------------------------

# 🔁 Imports Django
from django.db import models

# 🔁 Import du modèle utilisateur personnalisé
from accounts.models import CustomUser


# ---------------------------------------------------------------------
# 🧱 Modèle principal : Project
# ---------------------------------------------------------------------
class Project(models.Model):
    """
    Représente un projet publié par un client sur la plateforme CONTRACT-IT.
    Un projet peut être visible publiquement, ou attribué à un entrepreneur
    pour suivi et gestion. Il évolue dans le temps selon son statut.
    """

    # -----------------------------------------------------------------
    # 🔁 Statuts possibles pour un projet (menu déroulant dans l’admin)
    # -----------------------------------------------------------------
    STATUS_CHOICES = [
        ('active', 'Actif'),          # Projet publié, ouvert aux offres
        ('in_progress', 'En cours'),  # Projet attribué à un entrepreneur
        ('completed', 'Terminé'),     # Projet complété
        ('cancelled', 'Annulé'),      # Projet annulé ou retiré
    ]

    # -----------------------------------------------------------------
    # 🔒 Champ : visibilité publique ou privée
    # -----------------------------------------------------------------
    is_public = models.BooleanField(
        default=True,
        help_text="Le projet est-il visible publiquement ? (True = tous les entrepreneurs peuvent le voir)"
    )

    # -----------------------------------------------------------------
    # 👤 Client qui a publié le projet
    # -----------------------------------------------------------------
    client = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,          # Si le client est supprimé → champ devient NULL
        null=True,
        blank=True,
        related_name='projects_posted',     # Permet d’appeler client.projects_posted.all()
        limit_choices_to={'is_client': True},  # Restreint aux utilisateurs clients
        help_text="Utilisateur (client) qui a publié ce projet"
    )

    # -----------------------------------------------------------------
    # 👷 Entrepreneur sélectionné (facultatif au début)
    # -----------------------------------------------------------------
    contractor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,          # Si le contractor est supprimé → champ devient NULL
        null=True,
        blank=True,
        related_name='projects_awarded',    # Permet d’appeler contractor.projects_awarded.all()
        limit_choices_to={'is_contractor': True},  # Restreint aux utilisateurs entrepreneurs
        help_text="Utilisateur (entrepreneur) sélectionné pour ce projet (facultatif)"
    )

    # -----------------------------------------------------------------
    # 📌 Informations principales du projet
    # -----------------------------------------------------------------

    # 🏷️ Titre du projet
    title = models.CharField(
        max_length=255,
        help_text="Titre clair et court du projet (ex. : Rénovation salle de bain)"
    )

    # 📄 Description détaillée
    description = models.TextField(
        help_text="Description complète des travaux à réaliser"
    )

    # 🔧 Catégorie ou type de service (ex : toiture, plomberie…)
    category = models.CharField(
        max_length=100,
        help_text="Type de projet ou domaine requis (ex : Électricité, Peinture)"
    )

    # 📍 Localisation du chantier (ville, quartier ou adresse partielle)
    location = models.CharField(
        max_length=255,
        help_text="Lieu d'exécution des travaux (ville, région, etc.)"
    )

    # 💰 Budget estimé (peut être une fourchette future)
    budget = models.DecimalField(
        max_digits=10,  # Jusqu’à 9 999 999.99
        decimal_places=2,
        help_text="Budget estimé ou alloué pour le projet (en dollars CAD)"
    )

    # 📆 Échéance souhaitée
    deadline = models.DateField(
        help_text="Date limite souhaitée pour l’achèvement du projet"
    )

    # -----------------------------------------------------------------
    # 🔄 Suivi du cycle de vie
    # -----------------------------------------------------------------
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        help_text="Statut actuel du projet (actif, en cours, terminé ou annulé)"
    )

    # 🤖 Généré par IA ?
    ai_drafted = models.BooleanField(
        default=False,
        help_text="Ce projet a-t-il été rédigé automatiquement par l’assistant IA ?"
    )

    # 🕒 Date de publication initiale (création)
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date de création automatique lors de la publication"
    )

    # ✏️ Date de dernière mise à jour
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Mise à jour automatique à chaque modification"
    )

    # -----------------------------------------------------------------
    # 🔁 Représentation lisible d’un projet
    # -----------------------------------------------------------------
    def __str__(self):
        # Affiche le titre + statut dans l’admin ou en debug
        return f"{self.title} ({self.status})"

    # -----------------------------------------------------------------
    # ✅ Nombre total de jalons associés (utile dans l'admin ou pour tri)
    # -----------------------------------------------------------------
    @property
    def milestone_count(self):
        """
        Retourne le nombre de jalons liés à ce projet.
        Pratique pour affichage dans l’admin ou les templates HTML.
        """
        return self.milestones.count()


# 📁 Fichier : projects/models.py (ou un fichier milestones.py si séparé)
class Milestone(models.Model):
    """
    Représente un jalon (étape) dans un projet CONTRACT-IT.
    Chaque jalon peut être validé, payé et documenté indépendamment.
    """

    # 🔗 Projet associé à ce jalon
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,  # Si le projet est supprimé → tous ses jalons aussi
        related_name='milestones',
        help_text="Projet auquel ce jalon est rattaché"
    )

    # 🏷️ Nom ou titre du jalon (ex : Démolition, Installation électrique…)
    title = models.CharField(
        max_length=255,
        help_text="Titre du jalon"
    )

    # 📝 Détails du jalon
    description = models.TextField(
        blank=True,
        help_text="Détails précis sur les travaux associés à ce jalon"
    )

    # 💰 Montant prévu pour ce jalon
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Montant à verser à la complétion de ce jalon"
    )

    # 📅 Date prévue de livraison
    due_date = models.DateField(
        help_text="Date limite souhaitée pour compléter ce jalon"
    )

    # ✅ Statut du jalon
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminé'),
        ('approved', 'Approuvé'),
        ('paid', 'Payé'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Statut actuel du jalon"
    )

    # 🕒 Suivi des dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} — {self.project.title}"


# ---------------------------------------------------------------------
# 📁 Modèles : Portfolio de l'entrepreneur
#
# Cette section permet à un entrepreneur de gérer les projets qu’il
# souhaite afficher publiquement dans son profil CONTRACT-IT.
#
# Deux types de projets sont gérés :
#   - Externes (créés manuellement),
#   - Internes (réalisés via la plateforme CONTRACT-IT).
#
# Chaque modèle est documenté ligne par ligne.
# ---------------------------------------------------------------------

# 🔁 Imports supplémentaires nécessaires pour cette section
from decimal import Decimal
from django.core.exceptions import ValidationError

# ---------------------------------------------------------------------
# 📦 Modèle : ExternalPortfolioItem
# Représente un projet réalisé par l'entrepreneur EN DEHORS de la plateforme.
# Il est saisi manuellement via le dashboard de l'entrepreneur.
# ---------------------------------------------------------------------
class ExternalPortfolioItem(models.Model):
    # 🔗 Utilisateur propriétaire du projet (doit être un entrepreneur)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,  # 🔁 Si l'utilisateur est supprimé, ses projets le sont aussi
        related_name='external_portfolio_items',
        help_text="Utilisateur (entrepreneur) ayant réalisé ce projet externe."
    )

    # 🏷️ Titre du projet
    title = models.CharField(
        max_length=100,
        help_text="Titre court et explicite du projet externe (ex. : Rénovation cuisine 2023)."
    )

    # 📝 Description détaillée du projet
    description = models.TextField(
        blank=True,
        help_text="Description libre du projet (matériaux, durée, défis techniques…)."
    )

    # 📅 Date de réalisation du projet
    date = models.DateField(
        help_text="Date à laquelle le projet a été réalisé (mois ou année)."
    )

    # ⏱️ Durée estimée ou indiquée du projet
    duration = models.CharField(
        max_length=100,
        help_text="Durée totale du projet (ex. : 3 semaines, 2 mois)."
    )

    # 💰 Prix total du projet
    price = models.DecimalField(
        max_digits=10,  # 🔢 Jusqu’à 9 999 999.99
        decimal_places=2,
        help_text="Montant payé pour la réalisation du projet (en dollars CAD)."
    )

    # 📅 Date d’ajout du projet dans le portfolio (automatique)
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date d’enregistrement de ce projet dans le portfolio."
    )

    # 👁️ Indique si ce projet est visible publiquement dans le profil
    visible_in_portfolio = models.BooleanField(
        default=True,
        help_text="Ce projet est-il visible par les visiteurs du profil public ?"
    )

    def __str__(self):
        # 🎯 Affichage lisible dans l’admin et le debug
        return f"[EXTERNE] {self.title} - {self.user.get_display_name()}"

# ---------------------------------------------------------------------
# 🖼️ Modèle : ExternalPortfolioMedia
# Gère les images associées à un projet externe.
# Un projet externe peut avoir plusieurs images.
# ---------------------------------------------------------------------
class ExternalPortfolioMedia(models.Model):
    # 🔗 Projet externe auquel l’image est rattachée
    portfolio_item = models.ForeignKey(
        ExternalPortfolioItem,
        on_delete=models.CASCADE,  # 🔁 Supprime les images si le projet est supprimé
        related_name='media',
        help_text="Projet externe auquel cette image est associée."
    )

    # 🖼️ Image stockée dans le dossier media/portfolio/external/
    image = models.ImageField(
        upload_to='portfolio/external/',
        help_text="Fichier image illustrant le projet externe (ex. : photo avant/après)."
    )

    def __str__(self):
        # 🎯 Nom par défaut dans l’admin
        return f"Image de {self.portfolio_item.title}"

# ---------------------------------------------------------------------
# 🔗 Modèle : InternalPortfolioItem
# Représente un projet CONTRACT-IT réalisé via la plateforme
# que l’entrepreneur choisit d’ajouter à son portfolio.
# ---------------------------------------------------------------------
class InternalPortfolioItem(models.Model):
    # 🔗 Entrepreneur propriétaire du projet
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='internal_portfolio_items',
        help_text="Utilisateur ayant réalisé ce projet CONTRACT-IT."
    )

    # 🔗 Référence au projet réel (OneToOne pour éviter les doublons)
    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name='portfolio_item',
        help_text="Projet CONTRACT-IT à intégrer dans le portfolio."
    )

    # 📝 Commentaire libre de l'entrepreneur (non visible par défaut)
    notes = models.TextField(
        blank=True,
        help_text="Commentaire personnel de l’entrepreneur sur ce projet (visible publiquement)."
    )

    # 👁️ Switch : ce projet doit-il être affiché dans le portfolio public ?
    visible_in_portfolio = models.BooleanField(
        default=True,
        help_text="Ce projet est-il affiché dans le portfolio public ?"
    )

    # 🕒 Date d’ajout dans le portfolio
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date à laquelle ce projet a été ajouté au portfolio."
    )

    def clean(self):
        """
        ✅ Validation personnalisée :
        - Le projet doit être attribué à l’utilisateur courant.
        - Le projet doit être marqué comme complété.
        """
        if self.project.contractor != self.user:
            raise ValidationError("Ce projet n'est pas attribué à cet utilisateur.")
        if self.project.status != 'completed':
            raise ValidationError("Seuls les projets complétés peuvent être ajoutés au portfolio.")

    def __str__(self):
        # 🎯 Affichage lisible dans l’admin
        return f"[CONTRACT-IT] {self.project.title} - {self.user.get_display_name()}"
