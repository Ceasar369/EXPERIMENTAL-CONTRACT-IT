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
