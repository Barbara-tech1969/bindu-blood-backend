from rest_framework import serializers
from account.serializers import UserSerializer
from event.models import Event
from account.models import User

# User Details for Event
class UserDetailsSerializer(serializers.ModelSerializer):
  class Meta:
    model=User
    fields = ['username','email', 'first_name', 'last_name',  'image']


class EventSerializer(serializers.ModelSerializer):
  created_by = UserDetailsSerializer(many=False, read_only=True)
  class Meta:
    model = Event
    fields = ['title', 'banner', 'event_date', 'location', 'description', 'is_approved', 'slug', 'created_by', 'created_at', 'updated_at']
    read_only_fields = ['slug', 'created_by', 'is_approved', 'created_at', 'updated_at']
    extra_kwargs = {
      'description': {'required': False},  # Making description optional for POST/PUT
      'banner': {'required': False},  # Making banner optional for POST/PUT
    }