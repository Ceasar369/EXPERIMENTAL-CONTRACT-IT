# bids/serializers.py

from rest_framework import serializers
from .models import Bid

class BidSerializer(serializers.ModelSerializer):
    # 🔄 Nom de l'entrepreneur affiché automatiquement
    contractor_username = serializers.CharField(source='contractor.username', read_only=True)
    
    class Meta:
        model = Bid
        fields = [
            'id',
            'contractor',  # 🔐 ID du contracteur (sera défini automatiquement dans la vue)
            'contractor_username',  # 👤 Nom lisible dans les réponses API
            'project',  # 🔗 ID du projet ciblé
            'amount',  # 💲 Montant proposé
            'message',  # 📝 Message d'accompagnement
            'status',  # 🕐 Statut de l'offre
            'created_at',  # ⏱️ Date d'envoi
        ]
        read_only_fields = ['status', 'created_at']  # ✅ Le statut sera géré par le client via l'interface, pas modifiable par l'entrepreneur
