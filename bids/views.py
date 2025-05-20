# ---------------------------------------------------------------------
# 📁 Fichier : bids/views.py
#
# 🎯 Ce fichier regroupe toutes les vues HTML liées aux offres (bids)
#     soumises par les entrepreneurs sur des projets CONTRACT-IT.
#
# Les vues permettent :
#   - de soumettre une bid via un formulaire,
#   - d’afficher une page de confirmation après soumission,
#   - de voir les bids reçues pour un projet donné (côté client),
#   - de voir toutes les bids soumises par un entrepreneur connecté,
#   - d’accepter une bid (côté client).
#
# Aucune API, aucun JWT : uniquement du Django HTML classique.
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# 🔁 IMPORTS DJANGO
# ---------------------------------------------------------------------
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponseForbidden

# ---------------------------------------------------------------------
# 🔁 IMPORTS INTERNES
# ---------------------------------------------------------------------
from .models import Bid
from projects.models import Project

# ---------------------------------------------------------------------
# 1️⃣ SubmitBidFormView (vue CBV) : permet à l'entrepreneur de soumettre une bid
# ---------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class SubmitBidFormView(View):
    """
    Vue de soumission de bid, accessible uniquement aux entrepreneurs connectés.

    - GET : affiche le formulaire de proposition pour un projet donné.
    - POST : enregistre la proposition et redirige vers confirmation.
    """

    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id, is_public=True, status='active')

        return render(request, 'bids/submit_bid_form.html', {
            'project': project
        })

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id, is_public=True, status='active')

        # Données soumises par le formulaire
        amount = request.POST.get("amount")
        message = request.POST.get("message")

        # Création de la bid en base
        Bid.objects.create(
            project=project,
            contractor=request.user,
            amount=amount,
            message=message
        )

        return redirect('bids:bid_confirmation_view')


# ---------------------------------------------------------------------
# 2️⃣ bid_confirmation_view : page de confirmation après soumission
# ---------------------------------------------------------------------
@login_required
def bid_confirmation_view(request):
    """
    Affiche un message de confirmation après avoir soumis une bid.
    """
    return render(request, 'bids/bid_confirmation.html')


# ---------------------------------------------------------------------
# 3️⃣ project_bids_view : liste des bids reçues par un client pour un projet
# ---------------------------------------------------------------------
@login_required
def project_bids_view(request, project_id):
    """
    Permet au client propriétaire d’un projet de voir toutes les bids reçues.
    """
    project = get_object_or_404(Project, pk=project_id)

    if request.user != project.client:
        return render(request, "core/403.html", status=403)

    bids = Bid.objects.filter(project=project).order_by('-created_at')

    return render(request, 'bids/project_bids.html', {
        'project': project,
        'bids': bids,
    })


# ---------------------------------------------------------------------
# 4️⃣ my_bids_view : liste des bids soumises par l'entrepreneur connecté
# ---------------------------------------------------------------------
@login_required
def my_bids_view(request):
    """
    Affiche toutes les bids soumises par l'utilisateur connecté (entrepreneur uniquement).
    """
    if not request.user.is_contractor:
        return render(request, "core/403.html", status=403)

    bids = Bid.objects.filter(contractor=request.user).order_by('-created_at')

    return render(request, 'bids/my_bids.html', {
        'bids': bids
    })


# ---------------------------------------------------------------------
# 5️⃣ accept_bid_view : permet à un client d’accepter une offre spécifique
# ---------------------------------------------------------------------
@login_required
def accept_bid_view(request, bid_id):
    """
    Permet au client d'accepter une proposition.
    Change le statut de la bid en 'accepted' si les vérifications sont valides.
    """
    bid = get_object_or_404(Bid, id=bid_id)

    if bid.project.client != request.user:
        return HttpResponseForbidden("⛔ Accès refusé.")

    bid.status = 'accepted'
    bid.save()

    # TODO : activer une messagerie ici, notifier l’entrepreneur, etc.
    return redirect('bids:bid_accepted_confirmation_view')


# ---------------------------------------------------------------------
# 6️⃣ bid_accepted_confirmation_view : page de succès après acceptation
# ---------------------------------------------------------------------
@login_required
def bid_accepted_confirmation_view(request):
    """
    Affiche une simple page de confirmation après avoir accepté une bid.
    """
    return render(request, 'bids/bid_accepted_confirmation.html')
