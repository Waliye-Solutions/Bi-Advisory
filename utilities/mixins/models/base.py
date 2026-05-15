import uuid, os, logging
from typing import Optional
from functools import cached_property

from django.db import models
from django.conf import settings
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from utilities.utils import BaseUtils
from hitcount.models import HitCountMixin
from utilities.mixins.managers import BaseAbstractManager
from biadvisorytech.middlewares.auto import ThreadLocalUser


# UserModel = get_user_model()
logger = logging.getLogger(__name__)

class AbstractBaseModel(models.Model, HitCountMixin):
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=_("Marqué comme supprimé"))
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True, verbose_name=_("UUID"))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de création"))
    updated_on = models.DateTimeField(auto_now=True, verbose_name=_("Dernières modifications"))
    extra_data = models.JSONField(default=dict, blank=True, editable=False, verbose_name=_("Extra JSON"))
    
    
    obj_created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="created_%(class)s",
        verbose_name=_("Créé par"),
    )
    
    # by default (if none set), use the base manager
    objects = BaseAbstractManager()
    
    class Meta:
        abstract = True
        ordering = ["-created_on"]
    
    
    def save(self, *args, **kwargs):
        # auto discover user only on creation
        # if not self.pk and not self.obj_created_by:
        if not self.obj_created_by:
            try:
                self.obj_created_by = self.auto_detect_current_user(request=kwargs.pop("request", None))
            except Exception as e:
                logger.error(f"Error auto detecting current user: {e}")
        return super().save(*args, **kwargs)
    
    
    
    def extra_data_pretty(self):
        return BaseUtils.prettify_json_data(data=self.extra_data)
    extra_data_pretty.short_description = _("Extra Data JSON") # type: ignore
    
    
    @cached_property
    def created_by(self):
        return getattr(self, "obj_created_by", None)
    
    def delete(self, *args, **kwargs):
        """Supprimer le fichier associé lors de la suppression de l'instance"""
        file = self.get_file()
        if not file:
            return super().delete(*args, **kwargs)
        
        try:
            if os.path.isfile(file.path):
                os.remove(file.path)
        except Exception as e:
            logger.error(f"Error deleting file for {self}: {e}", exc_info=True)
        
        return super().delete(*args, **kwargs)
    
    def fake_delete(self, *args, **kwargs):
        self.is_deleted = True
        return self.save(*args, **kwargs)
    
    def get_file(self):
        """ A method to retrieve a file from the model instance """
        file = getattr(self, "file", None)
        if file and hasattr(file, "url"):
            return file
        return None
    
    def get_user_from_request(self, request: Optional[HttpRequest] = None):
        user = None
        if isinstance(request, HttpRequest):
            user = request.user
        
        try:
            user = self.request.user # type: ignore (no request attribute on model, but maybe set by caller)
        except Exception as e:
            user = ThreadLocalUser.get_current_user()
        return user
    
    
    def auto_detect_current_user(self, request: Optional[HttpRequest] = None):
        return self.get_user_from_request(request=request)
    
    @cached_property
    def created_at(self):
        return self.created_on
    
    @cached_property
    def updated_at(self):
        return self.updated_on
    
    @cached_property
    def get_name(self):
        name = getattr(self, "name", None)
        if isinstance(name, str):
            return name.strip()
        return self.__str__()
    
    @cached_property
    def get_str_repr(self):
        verbose_name = getattr(self._meta, "verbose_name_plural", None)
        return verbose_name or self.__class__.__name__
    
    @cached_property
    def views_count(self):
        hits = getattr(self.hit_count, "hits", 0)
        try:
            return int(hits)
        except:
            return 0
    
    @staticmethod
    def prettify_json_field(data):
        return BaseUtils.prettify_json_data(data=data)
