# accounts/views.py

# 🌐 Vues REST pour la gestion des comptes utilisateur (connexion, inscription, dashboard)

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RegisterSerializer, CustomUserSerializer
from .models import CustomUser
from .permissions import IsContractor  # ✅ Permission personnalisée pour restreindre l’accès aux entrepreneurs


# 🔐 Serializer personnalisé pour enrichir le JWT avec des infos utilisateur
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # 🔄 Génère un token JWT de base
        token = super().get_token(user)
        # ➕ Ajoute des infos supplémentaires au token (access token uniquement)
        token["username"] = user.username
        token["is_client"] = user.is_client
        token["is_contractor"] = user.is_contractor
        return token

    # ✅ On enrichit aussi la réponse JSON pour que le frontend sache le rôle utilisateur dès login
    def validate(self, attrs):
        # ✅ Valide les identifiants (username + password)
        data = super().validate(attrs)
        # ➕ Ajoute aussi ces infos dans la réponse JSON (pas juste dans le token)
        data["is_client"] = self.user.is_client
        data["is_contractor"] = self.user.is_contractor
        return data


# 🔐 Vue personnalisée pour la connexion (login)
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer  # Utilise le serializer ci-dessus
    permission_classes = [AllowAny]  # ✅ Pas besoin d’être connecté pour se connecter 😄


# 📝 Vue d'inscription d’un nouvel utilisateur
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer  # Ton RegisterSerializer complet (username, email, etc.)
    permission_classes = [AllowAny]  # ✅ Ouvert à tous (pas besoin d’être connecté)


# 💼 Dashboard REST pour entrepreneurs connectés uniquement
class ContractorDashboardView(APIView):
    # ✅ JWT obligatoire + utilisateur doit être un entrepreneur (grâce à IsContractor)
    permission_classes = [IsAuthenticated, IsContractor]

    def get(self, request):
        # 🔄 Sérialise l’utilisateur connecté
        serializer = CustomUserSerializer(request.user)
        # 📦 Renvoie les infos sous forme JSON
        return Response(serializer.data)
