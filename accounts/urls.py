# accounts/urls.py

from django.urls import path
from .views import LoginView, RegisterView, ContractorDashboardView, ClientDashboardView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # 🔐 Connexion JWT : renvoie access + refresh token (utilisé dans login.html et signup.html)
    path("login/", LoginView.as_view(), name="api-login"),

    # 🆕 Inscription d’un utilisateur (client ou entrepreneur)
    path("register/", RegisterView.as_view(), name="register"),

    # 💼 Dashboard REST côté entrepreneur (protégé par JWT)
    path('dashboard/contractor/', ContractorDashboardView.as_view(), name='contractor-dashboard'),

    # 💼 Dashboard REST côté client (protégé par JWT)
    path('dashboard/client/', ClientDashboardView.as_view(), name='client-dashboard'),

    # 🔁 Endpoint pour rafraîchir le token d’accès via un refresh token
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
