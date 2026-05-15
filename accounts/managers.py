import logging
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager

from accounts.utils import AccountUtils
from utilities.mixins.managers import BaseAbstractManager


logger = logging.getLogger(__name__)


class UserManager(BaseUserManager, BaseAbstractManager):
    def create_user(self, email: str, password=None, **extra_fields):
        if not email:
            raise ValueError(_("Veuillez fournir une adresse mail s'il vous plaît!"))
        
        if self.filter(email=str(email).lower()).exists():
            raise ValueError(_("Email déjà en cours d'utilisation"))
        
        username = AccountUtils.get_username_from_email(email=email, force_integrity=True)
        
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("username", username)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        
        try:
            user.save(using=self._db)
        except Exception as e:
            logger.error(f"Error creating user: {e}", exc_info=True)
            raise Exception(e)
        return user
    
    
    def create_superuser(self, email: str, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email=self.normalize_email(email), password=password, **extra_fields)
