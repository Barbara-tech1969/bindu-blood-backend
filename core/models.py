import sys
from django.db import models
from django.utils.text import slugify
from io import BytesIO  #basic input/output operation
from PIL import Image #Imported to compress images
from django.core.files.uploadedfile import InMemoryUploadedFile
# Create your models here.
#image compression method

class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True

class Service(TimeStampMixin):
    image = models.ImageField(
        upload_to="Bindu_Blood_Bank_Api/Services",
    )
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=350, unique=True, null=True, blank=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.image = self.compressImage(self.image)
        super().save(*args, **kwargs)
    def compressImage(self,image):
        imageTemproary = Image.open(image)
        outputIoStream = BytesIO()
        imageTemproary.resize( (1020,573) ) 
        imageTemproary.save(outputIoStream , format='Webp', quality=60)
        outputIoStream.seek(0)
        image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.webp" % image.name.split('.')[0], 'image/webp', sys.getsizeof(outputIoStream), None)
        return image
    
class ContactUs(TimeStampMixin):
    name = models.CharField(max_length = 30)
    email = models.EmailField(max_length=255)
    description = models.TextField()
    mark_as_done = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Contact Us"