from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from accounts.utils import AccountUtils
from accounts.managers import UserManager
from utilities.mixins.models import AbstractBaseModel


class User(AbstractUser, AbstractBaseModel): # type: ignore
    class GenderChoices(models.TextChoices):
        MALE = ("male", _("Masculin"))
        FEMALE = ("female", _("Féminin"))
        UNDEFINED = ("undefined", _("Non défini"))
    
    email = models.EmailField(max_length=100, unique=True, verbose_name=_("Adresse électronique"))
    first_name = models.CharField(max_length=255, verbose_name=_("Prénom(s)"), null=True, blank=True)
    last_name = models.CharField(max_length=255, verbose_name=_("Nom de famille"), null=True, blank=True)
    phone_number = models.CharField(max_length=255, verbose_name=_("Nº de téléphone"), null=True, blank=True)
    gender = models.CharField(choices=GenderChoices.choices, default=GenderChoices.UNDEFINED, null=True, max_length=10, verbose_name=_("Sexe"))
    role = models.CharField(max_length=100, verbose_name=_("Poste/Occupation"), null=True, blank=True)
    date_of_birth = models.DateField(verbose_name=_("Date de naissance"), null=True, blank=True)
    picture = models.ImageField(upload_to="accounts/avatars/%Y/", null=True, blank=True, verbose_name=_("Photo de profil"))
    bio = models.TextField(verbose_name=_("Biographie"), null=True, blank=True)
    
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = UserManager() # type: ignore
    
    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")
        ordering = ["-date_joined", "email", "first_name", "last_name", "gender", "date_of_birth", "username"]
    
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = AccountUtils.get_username_from_email(email=self.email, force_integrity=True)
        
        with transaction.atomic():
            return super().save(*args, **kwargs)
    
    
    @property
    def gender_is_male(self):
        return self.gender == self.GenderChoices.MALE
    
    @property
    def gender_is_female(self):
        return self.gender == self.GenderChoices.FEMALE
    
    @property
    def gender_is_undefined(self):
        return self.gender == self.GenderChoices.UNDEFINED
