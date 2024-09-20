from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

__all__ = ("Address", "User", 'State', 'Country')




class User(AbstractUser):
    phone_number = models.CharField(_("phone number"), max_length=15)
    date_of_birth = models.DateField(_("date of birth"), blank=True, null=True)
    is_verified = models.BooleanField(_("is verified"), default=False)

    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField("auth.Permission", related_name='custom_user_permissions', blank=True)


    def __str__(self):
        return self.username
    
    # class Meta(AbstractUser.Meta):
        # swappable = "AUTH_USER_MODEL"

class Country(models.Model):
    name = models.CharField(_("name"), max_length=100)
    iso_code = models.CharField(_("iso code"), max_length=2, unique=True)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countrys'

    def __str__(self):
        return f'{self.name}'


class State(models.Model):
    name = models.CharField(_("name"), max_length=255)
    country = models.ForeignKey("Country", verbose_name=_("country"), on_delete=models.CASCADE, related_name='state')

    class Meta:
        verbose_name = 'State'
        verbose_name_plural = 'States'

    def __str__(self):
        return f'{self.name}, {self.country.name}'


class Address(models.Model):
    """Address Model contain all the physical address imformation"""

    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE, related_name="address")
    address_line_1 = models.CharField(_("address line 1"), max_length=255)
    address_line_2 = models.CharField(_("address line 2"), max_length=255, blank=True, null=True)
    country = models.ManyToManyField(Country, verbose_name=_("country"), related_name="address")
    state = models.ManyToManyField(State, verbose_name=_("state"))
    city = models.CharField(_("city"), max_length=255)
    street_address = models.CharField(_("street address"), max_length=255)
    postal_code = models.CharField(_("postal code"), max_length=255)
    is_primary = models.BooleanField(_("is primary"), default=False)


    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresss'

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.country}"



