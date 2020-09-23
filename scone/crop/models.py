import os
import uuid

from django.db import models


class BaseModel(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Picture(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_filename = models.CharField(max_length=1024, null=True, blank=True, editable=False)
    extension = models.CharField(max_length=256, blank=True, null=True, editable=False)
    uri = models.CharField(max_length=2048, null=True, blank=True, unique=True)
    image = models.ImageField(upload_to='crop/picture/image')

    def __str__(self):
        return f'{self.original_filename or "Untitled"}'

    def save(self, *args, **kwargs):
        self.original_filename, self.extension = os.path.splitext(self.image.name)
        return super().save(*args, **kwargs)
