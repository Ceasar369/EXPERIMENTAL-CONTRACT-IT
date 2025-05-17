# ---------------------------------------------------------------------
# 📁 Fichier : bids/models.py
#
# 🎯 Ce fichier contient le modèle `Bid`, qui représente une soumission
#     faite par un entrepreneur pour un projet publié sur CONTRACT-IT.
#
# Chaque bid est associé à :
#     - un projet (`Project`) visé par la soumission,
#     - un entrepreneur (`CustomUser`) qui soumet son offre,
#     - un montant proposé + un message explicatif.
#
# Ce modèle est utilisé :
#     - pour afficher les offres reçues côté client,
#     - pour envoyer une offre depuis le côté entrepreneur,
#     - pour afficher une confirmation de soumission,
#     - et plus tard, pour gérer les validations, les contrats ou les paiements.
#
# Le modèle est simple mais efficace pour la version HTML.
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# 🔁 IMPORTS DJANGO
# ---------------------------------------------------------------------
from django.db import models                  # 🧱 Base des modèles Django
from django.conf import settings              # ⚙️ Pour utiliser AUTH_USER_MODEL
from projects.models import Project           # 🔗 Pour lier un bid à un projet

# ---------------------------------------------------------------------
# 🧾 Modèle : Bid (Soumission d’un entrepreneur pour un projet)
# ---------------------------------------------------------------------
class Bid(models.Model):
    """
    Représente une offre déposée par un entrepreneur (contractor)
    pour répondre à un projet publié sur la plateforme CONTRACT-IT.

    Inclut :
    - un lien vers le projet
    - un lien vers l’entrepreneur
    - un montant
    - un message d’accompagnement
    - un statut (pending, accepted, rejected)
    - la date de création
    """

    # 👤 L'entrepreneur qui soumet la bid
    contractor = models.ForeignKey(
        settings.AUTH_USER_MODEL,            # 🔗 Utilise le modèle utilisateur personnalisé
        on_delete=models.CASCADE,            # ❌ Supprimer l'utilisateur supprime aussi ses offres
        help_text="Entrepreneur ayant soumis cette offre"
    )

    # 📦 Le projet concerné par la proposition
    project = models.ForeignKey(
        Project,                             # 🔗 Relation vers un projet
        on_delete=models.CASCADE,           # ❌ Supprimer le projet supprime aussi les bids liées
        related_name='bids',                # Permet project.bids.all()
        help_text="Projet pour lequel cette offre a été soumise"
    )

    # 💵 Le montant proposé par l’entrepreneur
    amount = models.DecimalField(
        max_digits=10,                      # Ex. : 9999999.99
        decimal_places=2,
        help_text="Montant total proposé pour réaliser le projet"
    )

    # 📝 Message accompagnant l’offre
    message = models.TextField(
        help_text="Message explicatif du contracteur (motivation, délai, etc.)"
    )

    # 🧭 Statut de la soumission
    STATUS_CHOICES = [
        ('pending', 'En attente'),          # 🕐 En cours d'examen
        ('accepted', 'Acceptée'),           # ✅ Sélectionnée par le client
        ('rejected', 'Rejetée'),            # ❌ Refusée par le client
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Statut actuel de la soumission"
    )

    # 🕓 Date de création
    created_at = models.DateTimeField(
        auto_now_add=True,                 # ⏱️ Automatiquement définie lors de la création
        help_text="Date à laquelle l’offre a été soumise"
    )

    # 🔁 Représentation lisible dans l’interface admin ou en debug
    def __str__(self):
        # 📄 Exemple affiché : "Bid de ahmad pour Réfection de toiture"
        return f"Bid de {self.contractor} pour {self.project.title}"
