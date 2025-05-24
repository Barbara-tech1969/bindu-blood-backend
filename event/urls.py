from django.urls import path, include
from rest_framework import routers
from event.views import EventView

router = routers.DefaultRouter()
router.register('', EventView, basename='event-api')

urlpatterns = [
    path('', include(router.urls)),
]
