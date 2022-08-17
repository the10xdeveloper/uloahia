from django.db import models

# Create your models here.
from malls import MallTypeKind


class Mall(models.Model):
    name = models.CharField(max_length=256, unique=True)
    kind = models.CharField(max_length=32, choices=MallTypeKind.CHOICES)
    is_active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=256, unique=True)

    # default_location = CountryField

    class Meta:
        ordering = ("slug",)

    def __str__(self):
        return self.slug
