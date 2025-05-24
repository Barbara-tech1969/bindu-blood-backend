from rest_framework import serializers
from event.serializers import UserDetailsSerializer
from donation.models import DonationReport, DonationRequest
from rest_framework.exceptions import ValidationError
from datetime import datetime

class DonationRequestSerializer(serializers.ModelSerializer):
  created_by = UserDetailsSerializer(many=False, read_only=True)
  class Meta:
    model = DonationRequest
    fields = '__all__'
    read_only_fields = ['id','created_at','created_by','is_accepted']

class DonationReportSerializer(serializers.ModelSerializer):
  user = UserDetailsSerializer(many=False, read_only=True)
  event = DonationRequestSerializer(many=False, read_only=True)
  event_id = serializers.IntegerField( write_only=True)
  class Meta:
    model = DonationReport
    fields = ['created_at','user','event', 'event_id']