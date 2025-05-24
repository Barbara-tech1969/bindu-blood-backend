from django.shortcuts import render
from core.models import Service, ContactUs
from core.serializers import ServiceSerializer, ContactSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
# Create your views here.

class ServiceView(ModelViewSet):
  queryset = Service.objects.all()
  serializer_class = ServiceSerializer
  lookup_field='slug'
  def get_permissions(self):
    if self.request.method == "GET":
      return [AllowAny()]
    return [IsAdminUser()]
  
class ContactView(ModelViewSet):
  queryset = ContactUs.objects.all()
  serializer_class = ContactSerializer
  http_method_names = ('get', 'post','patch',)
  def get_permissions(self):
    if self.request.method == "POST":
      return [AllowAny()]
    return [IsAdminUser()]