from django.urls import path, include
from rest_framework import routers
from core.views import ServiceView, ContactView

router = routers.DefaultRouter()
router.register('services', ServiceView, basename='service-api')
router.register('contact', ContactView, basename='contact-api')
urlpatterns = [
  path('', include(router.urls)),
]
