import uuid

from django.db import models


class BaseModel(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Picture(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uri = models.CharField(max_length=2048, null=True, blank=True, unique=True, db_index=True)
    request_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.id}'


class Crop(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_picture = models.ForeignKey(
        'crop.Picture',
        db_index=True,
        related_name='crops',
        on_delete=models.CASCADE,
    )
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    request_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.id}'
