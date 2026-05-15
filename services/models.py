from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from utilities.mixins.models import AbstractBaseModel


class Service(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Nom du service"))
    icon = models.ImageField(upload_to="services/icons/", verbose_name=_("Icône du service"), null=True, blank=True,
        help_text=_("Téléchargez une icône pour représenter ce service"))
    picture = models.ImageField(upload_to="services/pictures/", verbose_name=_("Image du service"), null=True, blank=True,
        help_text=_("Téléchargez une image pour illustrer ce service"))
    summary = models.CharField(max_length=50, verbose_name=_("Résumé du service"), help_text=_("Un bref résumé (en quelques mots)"))
    description = models.TextField(verbose_name=_("Description complète"))
    
    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
    
    def __str__(self):
        return self.name
    
    @property
    def title(self):
        return self.name
    
    
    def get_absolute_url(self):
        return reverse("services:services-detail", kwargs={"service_id": self.pk})
