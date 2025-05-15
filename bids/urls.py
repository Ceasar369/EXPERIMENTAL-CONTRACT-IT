# bids/urls.py

from django.urls import path
from .views import SubmitBidView, BidsReceivedView, SubmitBidFormView, bid_confirmation_view, project_bids_view


urlpatterns = [
    path('submit/', SubmitBidView.as_view(), name='submit-bid'),
    path('project/<int:project_id>/bids/', BidsReceivedView.as_view(), name='bids-received'),
    path("submit/<int:project_id>/", SubmitBidFormView.as_view(), name="submit-bid-form"),
    path("submit/<int:project_id>/", SubmitBidFormView.as_view(), name="submit-bid-form"),
    path("confirmation/", bid_confirmation_view, name="bid-confirmation"),
    path('received/<int:project_id>/', BidsReceivedView.as_view(), name='bids-received'),
    path('view-bids/<int:project_id>/', project_bids_view, name='view-project-bids'),
]
