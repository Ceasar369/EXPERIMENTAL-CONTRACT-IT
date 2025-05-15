# bids/views.py

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Bid
from .serializers import BidSerializer
from .permissions import IsContractor, IsProjectOwner
from projects.models import Project

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
