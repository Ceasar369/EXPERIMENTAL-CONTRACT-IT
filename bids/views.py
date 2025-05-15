# bids/views.py

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Bid
from .serializers import BidSerializer
from .permissions import IsContractor, IsProjectOwner


# ✅ Vue pour soumettre une bid (uniquement les entrepreneurs)
class SubmitBidView(generics.CreateAPIView):
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated, IsContractor]

    def perform_create(self, serializer):
        # 🔒 On s'assure que le contracteur est bien l'utilisateur connecté
        serializer.save(contractor=self.request.user)


# ✅ Vue pour lister les bids reçus sur un projet donné (visible uniquement par le client propriétaire)
class BidsReceivedView(generics.ListAPIView):
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectOwner]

    def get_queryset(self):
        # 🔍 On récupère les offres (bids) liées à un projet spécifique
        project_id = self.kwargs.get('project_id')
        return Bid.objects.filter(project__id=project_id)


# ✅ Vue pour accepter une offre (bid) – client seulement
class AcceptBidView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsProjectOwner]

    def post(self, request, bid_id):
        try:
            # 🔍 On récupère le bid à partir de son ID
            bid = Bid.objects.get(id=bid_id)
            project = bid.project

            # 🔒 On vérifie que l'utilisateur est bien le client propriétaire du projet
            if project.client != request.user:
                return Response({'detail': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

            # ✅ Marquer le bid comme accepté
            bid.status = 'accepted'
            bid.save()

            # ❌ Marquer tous les autres bids comme rejetés (sauf celui accepté)
            Bid.objects.filter(project=project).exclude(id=bid_id).update(status='rejected')

            # 🔁 Mise à jour du projet : assigner le contracteur, changer le statut, rendre privé
            project.contractor = bid.contractor
            project.status = 'in_progress'
            project.is_public = False
            project.save()

            return Response({'detail': 'Bid accepted and project updated.'}, status=status.HTTP_200_OK)

        except Bid.DoesNotExist:
            return Response({'detail': 'Bid not found.'}, status=status.HTTP_404_NOT_FOUND)


# ✅ Vue complète GET + POST pour soumettre une bid
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Bid
from projects.models import Project

@method_decorator(login_required, name='dispatch')
class SubmitBidFormView(View):
    def get(self, request, project_id):
        # 🔍 On récupère le projet public actif correspondant
        project = get_object_or_404(Project, id=project_id, is_public=True, status='active')
        return render(request, 'bids/submit_bid_form.html', {'project': project})

    def post(self, request, project_id):
        # 🔁 Même logique de récupération du projet
        project = get_object_or_404(Project, id=project_id, is_public=True, status='active')

        # 🧾 Données récupérées depuis le formulaire POST
        title = request.POST.get("title")
        description = request.POST.get("description")
        amount = request.POST.get("amount")
        deadline = request.POST.get("deadline")
        message = request.POST.get("message")

        # ✅ Création de la proposition
        Bid.objects.create(
            project=project,
            contractor=request.user,
            amount=amount,
            message=message
        )

        # 🚀 Redirection vers la page de confirmation
        return redirect('bid-confirmation')


# ✅ Vue HTML simple de confirmation après soumission d'une bid
def bid_confirmation_view(request):
    return render(request, 'bids/bid_confirmation.html')

# bids/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Bid
from projects.models import Project

# ✅ Vue HTML pour afficher tous les bids reçus sur un projet spécifique
@login_required
def project_bids_view(request, project_id):
    # 🧱 On récupère le projet ou on renvoie 404 si introuvable
    project = get_object_or_404(Project, pk=project_id)

    # 🔐 Sécurité : seul le client owner peut voir les bids de ce projet
    if request.user != project.client:
        return render(request, "core/403.html", status=403)

    # 📦 On récupère tous les bids associés à ce projet
    bids = Bid.objects.filter(project=project).order_by('-created_at')

    return render(request, 'bids/project_bids.html', {
        'project': project,
        'bids': bids,
    })
