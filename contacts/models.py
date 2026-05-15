from django.db import models
from django.utils.translation import gettext_lazy as _

from utilities.mixins.models import AbstractBaseModel


class Contact(AbstractBaseModel):
    full_name = models.CharField(max_length=255, verbose_name=_("Nom"))
    email = models.EmailField(verbose_name=_("Email"))
    phone_number = models.CharField(max_length=20, verbose_name=_("Numéro de téléphone"))
    subject = models.CharField(max_length=255, verbose_name=_("Sujet"))
    message = models.TextField(verbose_name=_("Message"))
    
    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")
        ordering = [*AbstractBaseModel.Meta.ordering, "subject", "full_name"]
    
    def __str__(self):
        return f"{self.full_name} - {self.subject}"
