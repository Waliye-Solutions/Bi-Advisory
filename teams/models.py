from django.db import models
from django.utils.translation import gettext_lazy as _

from utilities.mixins.models import AbstractBaseModel


class Team(AbstractBaseModel):
    full_name = models.CharField(verbose_name=_("Nom"), max_length=255)
    role = models.CharField(verbose_name=_("Rôle"), max_length=255)
    picture = models.ImageField(verbose_name=_("Photo"), upload_to="teams/pictures/", null=True, blank=True)
    facebook = models.URLField(verbose_name=_("Facebook"), blank=True, null=True)
    twitter = models.URLField(verbose_name=_("Twitter"), blank=True, null=True)
    linkedin = models.URLField(verbose_name=_("LinkedIn"), blank=True, null=True)
    instagram = models.URLField(verbose_name=_("Instagram"), blank=True, null=True)
    
    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Membre de l'équipe")
        verbose_name_plural = _("Membres de l'équipe")
    
    def __str__(self):
        return self.full_name
    
    @property
    def photo(self):
        return self.picture
