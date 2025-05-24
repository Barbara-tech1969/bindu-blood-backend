from rest_framework import serializers
from core.models import Service, ContactUs
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['title', 'image', 'description', 'slug']
        read_only_fields = ['slug']

class ContactSerializer(serializers.ModelSerializer):
  class Meta:
    model = ContactUs
    fields = ['name', 'email', 'description']