from django.db import models
from core.models import TimeStampMixin
from account.models import User
# Create your models here.
class DonationRequest(TimeStampMixin):
  created_at = models.DateField(auto_now_add=True)
  created_by = models.ForeignKey(User, related_name="donation_request", on_delete=models.CASCADE)
  blood_group = models.CharField(max_length=10)
  location = models.CharField(max_length=255)
  description = models.TextField()
  is_accepted = models.BooleanField(default=False)
  def __str__(self) -> str:
    return f"{self.blood_group} by {self.created_by.get_full_name()}"
  class Meta:
    verbose_name_plural = "Donation Requests"
  
class DonationReport(TimeStampMixin):
  created_at = models.DateField(auto_now_add=True)
  user = models.ForeignKey(User, related_name="donation_report", on_delete=models.CASCADE)
  event = models.ForeignKey(DonationRequest, related_name="donation_report", on_delete=models.CASCADE)

  def __str__(self) -> str:
    return f"{self.user.get_full_name()}"