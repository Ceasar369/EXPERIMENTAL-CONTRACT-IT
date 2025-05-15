# bids/urls.py

from django.urls import path
from .views import SubmitBidView, BidsReceivedView

urlpatterns = [
    path('submit/', SubmitBidView.as_view(), name='submit-bid'),
    path('project/<int:project_id>/bids/', BidsReceivedView.as_view(), name='bids-received'),
]
