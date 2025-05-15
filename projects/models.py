# projects/models.py


from django.db import models
from accounts.models import CustomUser  # On utilise le modèle utilisateur personnalisé

# 🏗️ Modèle représentant un projet publié sur CONTRACT-IT
class Project(models.Model):
    # 🏷️ Liste des statuts possibles pour un projet
    STATUS_CHOICES = [
        ('active', 'Actif'),         # Projet visible et ouvert aux offres
        ('in_progress', 'En cours'), # Projet attribué à un entrepreneur
        ('completed', 'Terminé'),    # Projet terminé
        ('cancelled', 'Annulé'),     # Projet annulé
    ]

    # 🔒 Détermine si le projet est visible publiquement ou restreint au client + contractor
    is_public = models.BooleanField(
        default=True,
        help_text="Le projet est-il visible par tous (True) ou privé (False)"
    )


    # 👤 Le client qui a créé ce projet (doit être un utilisateur avec is_client = True)
    client = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,  # Si le client est supprimé, on garde le projet mais client devient NULL
        related_name='projects_posted',  # Permet de faire client.projects_posted.all()
        limit_choices_to={'is_client': True},
        null=True,  # ✅ Important pour que SET_NULL soit autorisé
        blank=True,  # ✅ Pour le support dans les formulaires admin
        help_text="Client qui a publié ce projet"
    )

    # 👷 L'entrepreneur sélectionné pour ce projet (optionnel au début)
    contractor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,  # Si l'entrepreneur est supprimé, on garde le projet mais contractor devient NULL
        null=True,
        blank=True,
        related_name='projects_awarded',  # Permet de faire contractor.projects_awarded.all()
        limit_choices_to={'is_contractor': True},
        help_text="Entrepreneur engagé pour ce projet (facultatif)"
    )

    # 📝 Titre court du projet (visible dans les listes)
    title = models.CharField(
        max_length=255,
        help_text="Titre du projet (ex. : Rénovation cuisine)"
    )

    # 📄 Description complète des travaux à effectuer
    description = models.TextField(
        help_text="Détails complets fournis par le client"
    )

    # 🛠️ Type ou catégorie de projet (ex. : toiture, peinture…)
    category = models.CharField(
        max_length=100,
        help_text="Spécialité demandée ou domaine du projet"
    )

    # 📍 Lieu où le projet doit être réalisé
    location = models.CharField(
        max_length=255,
        help_text="Adresse, ville ou région du chantier"
    )

    # 💰 Budget prévu par le client (en dollars)
    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Budget estimé pour la réalisation"
    )

    # 📆 Date limite souhaitée pour la fin du projet
    deadline = models.DateField(
        help_text="Date à laquelle le projet doit idéalement être terminé"
    )

    # 🔄 Statut du projet (actif, en cours, terminé ou annulé)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        help_text="État actuel du projet dans le cycle de vie"
    )

    # 🤖 Indique si l'IA a aidé à rédiger ce projet
    ai_drafted = models.BooleanField(
        default=False,
        help_text="Généré automatiquement par l'assistant IA ?"
    )

    # 🕒 Date de création automatique du projet
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date à laquelle le projet a été publié"
    )

    # ✏️ Mise à jour automatique à chaque modification
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Dernière mise à jour des informations du projet"
    )

    def __str__(self):
        # 🔁 Représentation lisible du projet
        return f"{self.title} ({self.status})"
