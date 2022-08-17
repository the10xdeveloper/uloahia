from django.db import models

from django.utils import timezone
from django_measurement.models import MeasurementField
from measurement.measures import Weight, Volume
from mptt.managers import TreeManager
from mptt.models import MPTTModel

# Create your models here.

# Model for products
from versatileimagefield.fields import VersatileImageField

from ecom.units import WeightUnits, VolumeUnits
from ecom.weighing import zero_weight, zero_volume
from products import ProductTypeKind


class Category(MPTTModel):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True, allow_unicode=True)
    description = models.TextField(blank=True)
    background_image = VersatileImageField(upload_to="category-backgrounds", blank=True, null=True)
    parent = models.ForeignKey("self", null=True, blank=True, related_name="children", on_delete=models.CASCADE)

    objects = models.Manager()
    tree = TreeManager()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True, allow_unicode=True)
    kind = models.CharField(max_length=32, choices=ProductTypeKind.CHOICES)
    has_variants = models.BooleanField(default=True)
    is_shipping_required = models.BooleanField(default=True)
    is_digital = models.BooleanField(default=False)
    weight = MeasurementField(measurement=Weight,
                              unit_choices=WeightUnits.CHOICES,
                              default=zero_weight)
    volume = MeasurementField(measurement=Volume,
                              unit_choices=VolumeUnits.CHOICES,
                              default=zero_volume)

    class Meta:
        ordering = ("slug",)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        class_ = type(self)
        return "<%s.%s(pk=%r, name=%r)>" % (
            class_.__module__,
            class_.__name__,
            self.pk,
            self.name,
        )


class ProductQuerySet(models.QuerySet):
    def published(self, ):
        pass

    def not_published(self):
        pass

    def published_with_variants(self):
        pass


class Product(models.Model):
    pass


class ProductVariant(models.Model):
    pass


class VariantMedia(models.Model):
    pass
