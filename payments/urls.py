# ---------------------------------------------
# 📁 Fichier : payments/urls.py
# ---------------------------------------------
# 🎯 Ce fichier définit les routes URL de l'app "payments"
# Deux vues sont accessibles :
#   - demande de paiement (contractor),
#   - approbation/refus de paiement (client).

from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Route pour que l'entrepreneur demande un paiement
    path('request/<int:milestone_id>/', views.request_payment_view, name='request-payment'),

    # Route pour que le client approuve ou refuse un paiement
    path('approve/<int:payment_id>/', views.approve_payment_view, name='approve-payment'),

     # Route pour que le client libère un paiement sans demande
    path('release/<int:milestone_id>/', views.release_payment_view, name='release-payment'),
]
