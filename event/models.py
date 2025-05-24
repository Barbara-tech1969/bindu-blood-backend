import sys
from django.db import models
from django.utils.text import slugify
from core.models import TimeStampMixin
from account.models import User
from io import BytesIO  #basic input/output operation
from PIL import Image #Imported to compress images
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.
class Event(TimeStampMixin):
  title = models.CharField(max_length=255)
  slug = models.SlugField(unique=True)
  created_by = models.ForeignKey(User, related_name='event', on_delete=models.CASCADE)
  is_approved = models.BooleanField(default=False)
  event_date = models.DateField()
  location = models.CharField()
  banner = models.ImageField(
        upload_to="Bindu_Blood_Bank_Api/events",
    )
  description = models.TextField()

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.title)
    self.banner = self.compressImage(self.banner)
    super().save(*args, **kwargs)
  def compressImage(self,banner):
        imageTemproary = Image.open(banner)
        outputIoStream = BytesIO()
        imageTemproary.resize( (1020,573) ) 
        imageTemproary.save(outputIoStream , format='Webp', quality=60)
        outputIoStream.seek(0)
        banner = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.webp" % banner.name.split('.')[0], 'image/webp', sys.getsizeof(outputIoStream), None)
        return banner

