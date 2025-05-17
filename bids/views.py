# ---------------------------------------------------------------------
# 📁 Fichier : bids/views.py
#
# 🎯 Ce fichier regroupe toutes les vues HTML liées aux offres (bids)
#     soumises par les entrepreneurs sur des projets CONTRACT-IT.
#
# Les vues permettent :
#   - de soumettre une bid via un formulaire (SubmitBidFormView),
#   - d’afficher une page de confirmation après soumission,
#   - de voir les bids reçues pour un projet donné (client),
#   - de voir toutes les bids soumises par un entrepreneur connecté.
#
# Aucune API, aucun JWT : uniquement du Django HTML classique.
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# 🔁 IMPORTS DJANGO
# ---------------------------------------------------------------------
from django.contrib.auth.decorators import login_required             # ✅ Pour protéger les vues
from django.utils.decorators import method_decorator                 # ✅ Pour protéger les classes-based views
from django.shortcuts import render, redirect, get_object_or_404     # 🔧 Fonctions de base
from django.views import View                                        # 🧱 Vue générique classique
from django.http import HttpResponseForbidden


# ---------------------------------------------------------------------
# 🔁 IMPORTS INTERNES
# ---------------------------------------------------------------------
from .models import Bid                                              # 📦 Modèle Bid
from projects.models import Project                                  # 🔗 Modèle Project


# ---------------------------------------------------------------------
# 1️⃣ SubmitBidFormView (Vue class-based) : GET + POST
# ---------------------------------------------------------------------
@method_decorator(login_required, name='dispatch')
class SubmitBidFormView(View):
    """
    Vue de soumission de bid, accessible uniquement aux entrepreneurs connectés.

    - GET : affiche le formulaire de proposition pour un projet donné.
    - POST : enregistre les données et redirige vers confirmation.
    """

    def get(self, request, project_id):
        # 🔎 On récupère le projet actif et public ciblé
        project = get_object_or_404(Project, id=project_id, is_public=True, status='active')

        # 🧾 On affiche la page avec les détails du projet pour soumission
        return render(request, 'bids/submit_bid_form.html', {'project': project})

    def post(self, request, project_id):
        # 🔍 On récupère le même projet (validation sécurité)
        project = get_object_or_404(Project, id=project_id, is_public=True, status='active')

        # 📤 Données envoyées via le formulaire HTML
        amount = request.POST.get("amount")
        message = request.POST.get("message")

        # ✅ On crée une nouvelle bid en base de données
        Bid.objects.create(
            project=project,
            contractor=request.user,
            amount=amount,
            message=message
        )

        # 🚀 Redirection vers page de confirmation
        return redirect('bid-confirmation')


# ---------------------------------------------------------------------
# 2️⃣ bid_confirmation_view : vue simple
# ---------------------------------------------------------------------
@login_required
def bid_confirmation_view(request):
    """
    Affiche un message de confirmation après avoir soumis une bid.
    """
    return render(request, 'bids/bid_confirmation.html')


# ---------------------------------------------------------------------
# 3️⃣ project_bids_view : liste des bids reçues pour un projet donné
# ---------------------------------------------------------------------
@login_required
def project_bids_view(request, project_id):
    """
    Permet au client propriétaire d’un projet de voir toutes les bids reçues.
    """

    # 🔍 On récupère le projet ciblé ou erreur 404
    project = get_object_or_404(Project, pk=project_id)

    # 🔐 Vérification : seul le client propriétaire peut voir les bids
    if request.user != project.client:
        return render(request, "core/403.html", status=403)

    # 📦 On récupère toutes les bids associées
    bids = Bid.objects.filter(project=project).order_by('-created_at')

    # 📄 On envoie les données au template HTML
    return render(request, 'bids/project_bids.html', {
        'project': project,
        'bids': bids,
    })


# ---------------------------------------------------------------------
# 4️⃣ my_bids_view : toutes les bids de l’entrepreneur connecté
# ---------------------------------------------------------------------

from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.shortcuts import render
from .models import Bid

@login_required
def my_bids_view(request):
    """
    Affiche tous les bids soumis par l'utilisateur connecté
    (doit être un entrepreneur). Liste triée du plus récent au plus ancien.
    """

    # 🔒 Vérifie que l’utilisateur est bien un entrepreneur
    if not request.user.is_contractor:
        return render(request, "core/403.html", status=403)

    # 🔍 Récupère toutes les bids liées à cet entrepreneur
    bids = Bid.objects.filter(contractor=request.user).order_by('-created_at')

    # 📄 Affiche la page avec les données
    return render(request, 'bids/my_bids.html', {
        'bids': bids
    })


# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
@login_required
def accept_bid_view(request, bid_id):
    """
    Permet au client d'accepter une proposition d'un entrepreneur.
    Change le statut de la bid de 'pending' à 'accepted', puis redirige
    vers une page de confirmation temporaire.
    """

    bid = get_object_or_404(Bid, id=bid_id)

    # 🔒 Vérifie que c’est bien le client propriétaire du projet
    if bid.project.client != request.user:
        return HttpResponseForbidden("⛔ Accès refusé.")

    # 🔁 Change le statut de la bid
    bid.status = 'accepted'
    bid.save()

    # 📨 (plus tard) une logique ici pour activer une messagerie

    # ✅ Redirige vers une page de confirmation
    return redirect('bid-accepted-confirmation')

@login_required
def bid_accepted_confirmation(request):
    """
    Affiche une simple page de confirmation que la bid a été acceptée.
    """
    return render(request, 'bids/bid_accepted_confirmation.html')
