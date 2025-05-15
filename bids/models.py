# bids/models.py

from django.db import models
from django.conf import settings
from projects.models import Project

class Bid(models.Model):
    # 🔗 L'entrepreneur qui soumet l'offre
    contractor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # 🔗 Le projet concerné par l'offre
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='bids')

    # 💲 Montant proposé par l'entrepreneur
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # 📝 Message d'accompagnement du contracteur
    message = models.TextField()

    # 🕐 Statut de l'offre : en attente, acceptée, rejetée
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Acceptée'),
        ('rejected', 'Rejetée'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    # ⏰ Date de soumission
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid de {self.contractor} pour {self.project.title}"
