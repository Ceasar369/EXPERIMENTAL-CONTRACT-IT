# projects/serializers.py

# 🔄 Sérialisation du modèle Project pour l'API REST (lecture + écriture)

from rest_framework import serializers
from .models import Project

# 🎁 Serializer principal pour le modèle Project
# Sert à convertir un objet Django Project <-> JSON pour l'API REST
class ProjectSerializer(serializers.ModelSerializer):

    # 🔒 Le champ client est en lecture seule, défini automatiquement par la vue
    # 🔒 Le champ contractor est aussi en lecture seule (défini après attribution du projet)
    class Meta:
        model = Project
        fields = [
            'id',               # ID unique du projet
            'title',            # Titre du projet
            'description',      # Description complète
            'category',         # Spécialité demandée
            'location',         # Lieu du chantier
            'budget',           # Budget prévu
            'deadline',         # Date limite du projet
            'status',           # Statut du projet (active, terminé, etc.)
            'ai_drafted',       # Indique si le projet a été généré par IA
            'client',           # Le client qui a publié le projet
            'contractor',       # L'entrepreneur sélectionné
            'created_at',       # Date de création
            'updated_at',       # Date de mise à jour
        ]

        # ⛔ Ces champs ne doivent pas être modifiables par l'utilisateur
        read_only_fields = ['client', 'contractor', 'created_at', 'updated_at']

    # 🔎 Validation personnalisée pour empêcher un budget nul ou négatif
    def validate_budget(self, value):
        if value <= 0:
            raise serializers.ValidationError("Le budget doit être supérieur à zéro.")
        return value
