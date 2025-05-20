# ---------------------------------------------
# 📁 Fichier : payments/views.py
# ---------------------------------------------
# 🎯 Vues liées aux demandes de paiement.
# Ce fichier gère :
#   - la création d'une demande de paiement par l'entrepreneur,
#   - l'approbation ou le refus (avec motif) par le client,
#   - la libération directe d’un paiement par le client sans demande préalable.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import PaymentRequest
from projects.models import Milestone
from .forms import PaymentRequestForm, PaymentRefusalForm

# ------------------------------------------------------------------
# Vue : un entrepreneur demande le paiement d’un jalon (milestone)
# ------------------------------------------------------------------
@login_required
def request_payment_view(request, milestone_id):
    milestone = get_object_or_404(Milestone, id=milestone_id)

    # ✅ Vérifie que l'utilisateur connecté est bien l'entrepreneur associé au projet
    if request.user != milestone.project.contractor:
        return redirect('unauthorized')

    # ✅ Protection : empêche de soumettre plusieurs demandes pour le même jalon
    if hasattr(milestone, 'payment_request'):
        messages.error(request, "⚠️ Une demande de paiement a déjà été soumise pour ce jalon.")
        return render(request, 'payments/request_payment.html', {
            'form': PaymentRequestForm(),  # formulaire vide
            'milestone': milestone
    })



    # 📩 Traitement du formulaire POST (soumission du formulaire)
    if request.method == 'POST':
        form = PaymentRequestForm(request.POST, request.FILES)
        if form.is_valid():
            # Enregistre la demande sans valider tout de suite
            payment = form.save(commit=False)
            payment.milestone = milestone
            payment.contractor = request.user
            payment.save()
            messages.success(request, "🎉 Demande de paiement envoyée avec succès.")
            return redirect('contractor_dashboard_view')
    else:
        form = PaymentRequestForm()

    # 📄 Affichage du formulaire vierge en GET
    return render(request, 'payments/request_payment.html', {
        'form': form,
        'milestone': milestone
    })

# ------------------------------------------------------------------
# Vue : le client approuve ou refuse une demande de paiement reçue
# ------------------------------------------------------------------
@login_required
def approve_payment_view(request, payment_id):
    payment = get_object_or_404(PaymentRequest, id=payment_id)

    # 🔐 Vérifie que seul le client du projet peut accéder à cette vue
    if request.user != payment.milestone.project.client:
        return redirect('unauthorized')

    # ✅ Empêche l'utilisateur d'approuver ou refuser plusieurs fois
    if payment.approved:
        messages.info(request, "✅ Ce paiement a déjà été approuvé.")
        return redirect('client_dashboard_view')
    if payment.declined:
        messages.warning(request, "❌ Ce paiement a déjà été refusé.")
        return redirect('client_dashboard_view')

    # 📩 Traitement du POST (action approuver ou refuser)
    if request.method == 'POST':
        if 'approve' in request.POST:
            payment.approved = True
            payment.approved_at = timezone.now()
            payment.save()
            messages.success(request, "✅ Paiement approuvé.")
            return redirect('client_dashboard_view')
        elif 'decline' in request.POST:
            form = PaymentRefusalForm(request.POST, instance=payment)
            if form.is_valid():
                payment = form.save(commit=False)
                payment.declined = True
                payment.declined_at = timezone.now()
                payment.save()
                messages.warning(request, "❌ Demande refusée avec commentaires transmis à l’entrepreneur.")
                return redirect('client_dashboard_view')
    else:
        form = PaymentRefusalForm(instance=payment)

    # 🖥️ Affichage du formulaire de validation/refus
    return render(request, 'payments/approve_payment.html', {
        'payment': payment,
        'form': form
    })

# ------------------------------------------------------------------
# Vue : le client libère directement un paiement sans demande officielle
# ------------------------------------------------------------------
@login_required
def release_payment_view(request, milestone_id):
    milestone = get_object_or_404(Milestone, id=milestone_id)

    # 🔐 Vérifie que seul le client peut effectuer ce type de paiement
    if request.user != milestone.project.client:
        return redirect('unauthorized')

    # ✅ Vérifie qu'aucune demande officielle n’existe déjà
    if PaymentRequest.objects.filter(milestone=milestone).exists():
        messages.info(request, "Une demande de paiement existe déjà pour ce jalon.")
        return redirect('client_dashboard_view')

    # ✅ Crée une PaymentRequest automatiquement (sans fichier ni description)
    PaymentRequest.objects.create(
        milestone=milestone,
        contractor=milestone.project.contractor,
        approved=True,
        approved_at=timezone.now(),
        description="Paiement libéré directement par le client sans demande préalable."
    )

    messages.success(request, "✅ Paiement libéré manuellement pour ce jalon.")
    return redirect('client_dashboard_view')
