from django.urls import path, include
from rest_framework import routers
from donation.views import DonationRequestView, DonationReportView

router = routers.DefaultRouter()
router.register('request', DonationRequestView, basename='donation-request-api')
router.register('report', DonationReportView, basename='donation-report-api')

urlpatterns = [
  path('', include(router.urls)),
]