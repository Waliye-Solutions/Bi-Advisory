from django.db import models
from django.utils.translation import gettext_lazy as _

from utilities.mixins.models import AbstractBaseModel


class Newsletter(AbstractBaseModel):
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    is_subscribed = models.BooleanField(default=True, verbose_name=_("Abonné(e)"))
    
    class Meta(AbstractBaseModel.Meta):
        ordering = [*AbstractBaseModel.Meta.ordering, "email"]
        verbose_name = _("Newsletter")
        verbose_name_plural = _("Newsletter")
    
    def __str__(self):
        return self.email
