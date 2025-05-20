# ---------------------------------------------
# 📁 Fichier : payments/models.py
# ---------------------------------------------
# 🎯 Ce modèle représente une demande de paiement pour un jalon (milestone).
# Chaque jalon ne peut avoir qu'une seule demande de paiement liée.
# Ce modèle enregistre :
#   - le jalon concerné,
#   - l'entrepreneur qui fait la demande,
#   - la description du travail effectué,
#   - une image justificative optionnelle,
#   - les statuts de validation ou de refus du paiement,
#   - la raison du refus et les demandes du client si applicable,
#   - une logique automatique : si aucune réponse n'est donnée par le client après 14 jours,
#     le paiement est automatiquement approuvé.

from django.db import models
from django.conf import settings
from django.utils import timezone
from projects.models import Milestone

class PaymentRequest(models.Model):
    # Lien vers le jalon pour lequel le paiement est demandé (1-1 obligatoire)
    milestone = models.OneToOneField(Milestone, on_delete=models.CASCADE, related_name='payment_request')

    # L'entrepreneur qui fait la demande
    contractor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment_requests')

    # Description du travail effectué ou du contexte de la demande
    description = models.TextField(blank=True)

    # Image optionnelle en pièce justificative (ex : photo du travail réalisé)
    image = models.ImageField(upload_to='payment_proofs/', blank=True, null=True)

    # Date à laquelle la demande a été faite
    requested_at = models.DateTimeField(auto_now_add=True)

    # Statut de validation par le client
    approved = models.BooleanField(default=False)

    # Date d'approbation (si approuvé)
    approved_at = models.DateTimeField(null=True, blank=True)

    # Statut explicite pour un refus manuel par le client
    declined = models.BooleanField(default=False)

    # Date de refus (facultative)
    declined_at = models.DateTimeField(null=True, blank=True)

    # Raison du refus fournie par le client (ex : travaux incomplets, mal réalisés, etc.)
    refusal_reason = models.TextField(blank=True)

    # Recommandations ou demandes du client pour corriger ou compléter le jalon
    client_requests = models.TextField(blank=True)

    def is_pending(self):
        """
        Méthode utilitaire : indique si la demande est encore en attente d'une décision.
        """
        return not self.approved and not self.declined

    def should_auto_approve(self):
        """
        Vérifie si la demande a dépassé 14 jours sans réponse → à approuver automatiquement.
        """
        if self.is_pending():
            delta = timezone.now() - self.requested_at
            return delta.days >= 14
        return False

    def __str__(self):
        return f"Demande de paiement pour le jalon {self.milestone.id} (Approuvée : {self.approved})"
