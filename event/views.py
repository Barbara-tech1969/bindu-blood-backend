from django.shortcuts import render
from event.models import Event
from account.models import User
from event.serializers import EventSerializer
from event.permissions import EventPermission
from rest_framework import viewsets

# Create your views here.

class EventView(viewsets.ModelViewSet):
  queryset = Event.objects.all()
  permission_classes = (EventPermission,)
  serializer_class = EventSerializer
  lookup_field = 'slug'
  http_method_names = ('post','get','delete','patch')
  def perform_create(self, serializer):
    return serializer.save(created_by=User.objects.get(username="admin"))
