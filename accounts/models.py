import datetime

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import model_to_dict
from django.urls import reverse
from django.utils.text import slugify
from django_countries.fields import CountryField, Country
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber
from django.db.models import Value
from versatileimagefield.fields import VersatileImageField

from . import Gender
from .validators import validate_possible_number

# Create your models here.

# Manager to manage and create users.
from malls import MallTypeKind


class MobileNumberField(PhoneNumberField):
    default_validators = [validate_possible_number]


class AddressQueryset(models.QuerySet):

    def annotate_default(self, user):
        # Set default shipping/billing address pk to None
        # if default shipping/billing address doesn't exist
        default_shipping_address_pk, default_billing_address_pk = None, None
        if user.default_shipping_address:
            default_shipping_address_pk = user.default_shipping_address.pk
        if user.default_billing_address:
            default_billing_address_pk = user.default_billing_address.pk

        return user.addresses.annotate(
            user_default_shipping_address_pk=Value(
                default_shipping_address_pk, models.IntegerField()
            ),
            user_default_billing_address_pk=Value(
                default_billing_address_pk, models.IntegerField()
            ),
        )


class Address(models.Model):
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    company_name = models.CharField(max_length=256, blank=True)
    street_address_1 = models.CharField(max_length=256, blank=True)
    street_address_2 = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=True)
    city_area = models.CharField(max_length=128, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = CountryField()
    country_area = models.CharField(max_length=128, blank=True)
    phone = MobileNumberField(blank=True, default="", db_index=True)

    objects = models.Manager.from_queryset(AddressQueryset)()

    class Meta:
        ordering = ("pk",)

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        if self.company_name:
            return "%s - %s" % (self.company_name, self.full_name)
        return self.full_name

    def __eq__(self, other):
        if not isinstance(other, Address):
            return False
        return self.as_data() == other.as_data()

    __hash__ = models.Model.__hash__

    def as_data(self):
        """Return the address as a dict suitable for passing as kwargs.

        Result does not contain the primary key or an associated user.
        """
        data = model_to_dict(self, exclude=["id", "user"])
        if isinstance(data["country"], Country):
            data["country"] = data["country"].code
        if isinstance(data["phone"], PhoneNumber):
            data["phone"] = data["phone"].as_e164
        return data

    def get_copy(self):
        """Return a new instance of the same address."""
        return Address.objects.create(**self.as_data())


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, first_name, last_name, password=None, is_active=True, is_superuser=False,
                    is_staff=False, is_admin=False,
                    is_vendee=False, is_vendor=False, is_dispatcher=False):
        if not email:
            raise ValueError("Sorry!, an email address is needed. Please provide one.")
        if not password:
            raise ValueError("Sorry!, an alphanumeric password must be  provided.")
        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.superuser = is_superuser
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self.db)
        return user

    def create_staff(self, email, first_name, last_name, password=None):
        user = self.create_user(email, first_name=first_name, last_name=last_name, password=password, is_staff=True)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(email, first_name=first_name, last_name=last_name, password=password, is_superuser=True,
                                is_staff=True, is_vendor=True, is_vendee=True, is_dispatcher=True, is_admin=True)
        return user


# Model defining the end usersÒ
class WebUser(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(unique=True, verbose_name='Email address')
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    addresses = models.ManyToManyField(Address, blank=True, related_name='user_addresses')
    avatar = VersatileImageField(upload_to="user-avatars", blank=True, null=True)
    birth_date = models.DateField(verbose_name='Birth date', blank=True, null=True, default=datetime.date.today)
    gender = models.CharField(choices=Gender.CHOICES, max_length=36, default="Male", null=True, blank=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    is_vendee = models.BooleanField(default=False, verbose_name="Vendee Account")
    is_vendor = models.BooleanField(default=False, verbose_name='Vendor Account')
    is_dispatcher = models.BooleanField(default=False, verbose_name="Dispatcher Account")
    is_active = models.BooleanField(default=True, verbose_name="Active Account")
    last_login = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = AccountManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.first_name and self.last_name:
            return F"{self.first_name} {self.last_name}"
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def vendee(self):
        return self.is_vendee

    @property
    def vendor(self):
        return self.is_vendor

    @property
    def dispatcher(self):
        return self.is_dispatcher

    def check_active(self):
        if self.is_active:
            return "Your account is Active!"
        else:
            return "Your account is not Activated!"


class Vendor(models.Model):
    user = models.OneToOneField(WebUser, on_delete=models.CASCADE, primary_key=True)
    business_name = models.CharField(max_length=256)
    business_type = models.CharField(max_length=32, choices=MallTypeKind.CHOICES, default='SUPERMARKET')

    class Meta:
        verbose_name_plural = 'Vendors'

    def __str__(self):
        if self.user.email:
            return self.user.email
        return self.business_name

    def get_absolute_url(self):
        kwargs = {"pk": self.pk}
        return reverse("vendors:vendor-detail", kwargs=kwargs)

    # def generate_slug(self):
    #     max_length = 256
    #     value = self.business_name
    #     slug_candidate = slug_original = slugify(value, allow_unicode=True)[:max_length]
    #     for i in itertools.count(1):
    #         if not Vendor.objects.filter(slug=slug_candidate).exists():
    #             break
    #         id_length = len(str(i)) + 1
    #         new_slug_text_part_length = len(slug_original) - id_length
    #         original_slug_with_id_length = len(slug_original) + id_length
    #
    #         candidate_slug_part = slug_original[
    #                               :new_slug_text_part_length] if original_slug_with_id_length > max_length else slug_original
    #         slug_candidate = "{}-{}".format(candidate_slug_part, i)
    #
    #     self.slug = slug_candidate
    #
    # def slug_length(self):
    #     return len(self.slug)
    #
    # def get_absolute_url(self):
    #     return reverse("vendors:vendor-detail", args=[str(self.slug)])
    #
    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.generate_slug()
    #
    #     super().save(*args, **kwargs)
    #
    #     pass


class Vendee(models.Model):
    user = models.OneToOneField(WebUser, on_delete=models.CASCADE, primary_key=True)
    default_shipping_address = models.ForeignKey(
        Address, related_name="+", null=True, blank=True, on_delete=models.SET_NULL)
    default_billing_address = models.ForeignKey(
        Address, related_name="+", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'Vendee'

    def __str__(self):
        if self.user.email:
            return self.user.email
        return self.user.first_name

    pass
