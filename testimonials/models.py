from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField
from utilities.mixins.models import AbstractBaseModel


class Testimonial(AbstractBaseModel):
    client_name = models.CharField(_("Nom du client"), max_length=255)
    client_position = models.CharField(_("Position du client"), max_length=255)
    client_country = CountryField(_("Pays"), help_text=_("Sélectionnez le pays du client"))
    client_picture = models.ImageField(_("Photo du client"), upload_to="testimonials/%Y/%m/", blank=True, null=True)
    stars = models.PositiveSmallIntegerField(_("Étoiles"), default=5, validators=[MaxValueValidator(5)])
    feedback = models.TextField(_("Feedback du client"))
    
    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Témoignage")
        verbose_name_plural = _("Témoignages")
    
    def __str__(self):
        return f"{self.client_name} - {self.stars} étoiles"
