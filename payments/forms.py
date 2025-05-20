from django import forms
from .models import PaymentRequest

# Formulaire pour envoyer une demande de paiement
class PaymentRequestForm(forms.ModelForm):
    class Meta:
        model = PaymentRequest
        fields = ['description', 'image']
        labels = {
            'description': "Description des travaux effectués",
            'image': "Preuve visuelle (facultative)"
        }

# Formulaire pour refuser une demande de paiement
class PaymentRefusalForm(forms.ModelForm):
    class Meta:
        model = PaymentRequest
        fields = ['refusal_reason', 'client_requests']
        labels = {
            'refusal_reason': "Motif du refus",
            'client_requests': "Travaux ou modifications demandés à l'entrepreneur"
        }
