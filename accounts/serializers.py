# accounts/serializers.py

from rest_framework import serializers
from .models import CustomUser

# 🎯 Serializer pour inscrire un nouvel utilisateur
# Ce serializer transforme les données JSON reçues lors de l’inscription
# en un objet CustomUser (utilisateur de la base de données)
class RegisterSerializer(serializers.ModelSerializer):
    # 🔐 Le mot de passe est requis et ne sera jamais renvoyé dans les réponses
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser  # On utilise le modèle personnalisé que tu as défini
        fields = (
            "username",          # Nom d'utilisateur unique
            "email",             # Adresse courriel de l'utilisateur
            "password",          # Mot de passe sécurisé (non lisible)
            "is_client",         # ✅ Booléen indiquant si c’est un client
            "is_contractor",     # ✅ Booléen indiquant si c’est un entrepreneur
            "phone",             # Numéro de téléphone (optionnel)
            "city"               # Ville de résidence (optionnel)
        )

    def create(self, validated_data):
        # 👤 On utilise create_user() pour s'assurer que le mot de passe est bien haché
        user = CustomUser.objects.create_user(
            username=validated_data["username"],        # Nom d'utilisateur
            email=validated_data["email"],              # Email unique
            password=validated_data["password"],        # Mot de passe (sera haché automatiquement)
            is_client=validated_data.get("is_client", False),       # Client ou non
            is_contractor=validated_data.get("is_contractor", False),  # Entrepreneur ou non
            phone=validated_data.get("phone", ""),      # Téléphone si fourni
            city=validated_data.get("city", ""),        # Ville si fournie
        )
        return user  # ✅ On retourne l'utilisateur nouvellement créé

    

# 📦 Serializer pour représenter un utilisateur (CustomUser) côté API
# Il permet de convertir un objet utilisateur Django <-> JSON
class CustomUserSerializer(serializers.ModelSerializer):

    # 🔧 Configuration du serializer
    class Meta:
        model = CustomUser  # On sérialise le modèle CustomUser
        fields = [  # Champs à inclure dans la réponse JSON
            'id', 'username', 'email',  # Champs de base
            'is_client', 'is_contractor',  # Rôles de l'utilisateur

            # Champs communs
            'phone', 'profile_picture', 'bio', 'city', 'language',
            'is_verified',

            # Champs spécifiques aux entrepreneurs
            'specialties', 'hourly_rate', 'availability', 'certifications',

            # Champ partagé : peut s’appliquer aux clients et aux entrepreneurs
            'company_name',

            # Champs spécifiques aux clients
            'project_history_count',

            'date_joined',  # Date d'inscription
        ]

        # ⛔ Ces champs sont en lecture seule : ils ne peuvent pas être modifiés via l’API
        read_only_fields = ['id', 'date_joined', 'is_verified']

    # 🔍 On filtre dynamiquement les champs du JSON selon le rôle de l’utilisateur connecté
    def to_representation(self, instance):
        # Appelle la méthode par défaut pour générer les données
        data = super().to_representation(instance)

        # 🔒 Si l'utilisateur N'EST PAS entrepreneur, on retire les champs entrepreneurs du JSON
        if not instance.is_contractor:
            contractor_fields = ['specialties', 'hourly_rate', 'availability', 'certifications']
            for field in contractor_fields:
                data.pop(field, None)

        # 🔒 Si l'utilisateur N'EST PAS client, on retire les champs réservés aux clients
        if not instance.is_client:
            client_only_fields = ['project_history_count']
            for field in client_only_fields:
                data.pop(field, None)

        # On retourne la version finale filtrée du JSON
        return data


# 🔄 Serializer pour permettre à un utilisateur de mettre à jour son profil
# Ce serializer applique des règles de validation selon que l'utilisateur est client, entrepreneur, ou les deux.
class CustomUserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser  # Le modèle de base est ton modèle utilisateur personnalisé
        fields = [  # Liste des champs que l'utilisateur peut modifier via l'API
            'phone',             # Numéro de téléphone
            'profile_picture',   # Photo de profil
            'bio',               # Description courte
            'city',              # Ville
            'language',          # Langue de l'interface
            'specialties',       # Spécialités (si entrepreneur)
            'hourly_rate',       # Tarif horaire (si entrepreneur)
            'availability',      # Disponibilité (si entrepreneur)
            'certifications',    # Certifications (si entrepreneur)
            'company_name',      # ✅ Visible pour tous (client ou entrepreneur)
            'project_history_count',  # Nombre de projets réalisés (si client)
        ]

    # 🔎 Validation personnalisée selon le rôle de l'utilisateur
    def validate(self, data):
        user = self.instance  # On récupère l'utilisateur actuellement modifié

        # ❌ Si l'utilisateur n'est PAS entrepreneur...
        if not user.is_contractor:
            # Liste des champs réservés aux entrepreneurs
            contractor_fields = ['specialties', 'hourly_rate', 'availability', 'certifications']
            for field in contractor_fields:
                # Si un champ réservé est dans la requête, on bloque
                if field in data:
                    raise serializers.ValidationError({
                        field: "Ce champ est réservé aux entrepreneurs."
                    })

        # ❌ Si l'utilisateur n'est PAS client...
        if not user.is_client:
            # Champs réservés aux clients
            client_only_fields = ['project_history_count']
            for field in client_only_fields:
                # Si un champ client est envoyé mais l'utilisateur n'est pas client → erreur
                if field in data:
                    raise serializers.ValidationError({
                        field: "Ce champ est réservé aux clients."
                    })

        return data  # ✅ Tous les champs sont valides : on retourne les données

