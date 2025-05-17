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
from django.db import models               # 🧱 Modèles de base Django
from django.conf import settings           # ⚙️ Pour référencer AUTH_USER_MODEL de façon générique
from projects.models import Project        # 🔗 Import du modèle Project (chaque bid est lié à un projet)


# ---------------------------------------------------------------------
# 🧾 Modèle : Bid (Soumission d’un entrepreneur pour un projet)
# ---------------------------------------------------------------------
class Bid(models.Model):
    """
    Représente une offre déposée par un entrepreneur (contractor)
    pour répondre à un projet publié sur la plateforme.

    Elle contient un montant proposé, un message explicatif,
    un statut de traitement (en attente, accepté, rejeté),
    et une date de création.
    """

    # 🔗 Utilisateur qui soumet l'offre (doit être un entrepreneur)
    contractor = models.ForeignKey(
        settings.AUTH_USER_MODEL,           # 🧑 Utilisateur relié
        on_delete=models.CASCADE,           # ❌ Si l'utilisateur est supprimé → bid supprimée
        help_text="Entrepreneur ayant soumis cette offre"
    )

    # 🔗 Projet ciblé par la proposition
    project = models.ForeignKey(
        Project,                            # 📦 Modèle Project lié
        on_delete=models.CASCADE,          # ❌ Si le projet est supprimé → les offres aussi
        related_name='bids',               # 🔁 Permet project.bids.all()
        help_text="Projet pour lequel cette offre a été soumise"
    )

    # 💰 Montant proposé par l’entrepreneur
    amount = models.DecimalField(
        max_digits=10,                     # 💸 Ex: 9999999.99
        decimal_places=2,
        help_text="Montant total proposé pour réaliser le projet"
    )

    # 📝 Message personnalisé accompagnant la proposition
    message = models.TextField(
        help_text="Message explicatif du contracteur (motivation, délai, etc.)"
    )

    # 🧭 Statut de traitement de la soumission
    STATUS_CHOICES = [
        ('pending', 'En attente'),         # 🕐 En attente de décision
        ('accepted', 'Acceptée'),          # ✅ Sélectionnée
        ('rejected', 'Rejetée'),           # ❌ Refusée
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Statut actuel de la soumission"
    )

    # 🕒 Date de soumission de l’offre (définie automatiquement)
    created_at = models.DateTimeField(
        auto_now_add=True,                # 🗓️ Date enregistrée automatiquement à la création
        help_text="Date à laquelle l’offre a été soumise"
    )

    # 🔁 Affichage lisible dans l’interface admin
    def __str__(self):
        # 📄 Exemple : "Bid de ahmad pour Réfection de toiture"
        return f"Bid de {self.contractor} pour {self.project.title}"
