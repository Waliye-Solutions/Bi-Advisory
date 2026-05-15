from django.db import models
from django.utils import timezone


class BaseAbstractQuerySet(models.QuerySet):
    """
    Base QuerySet for all models.
    Before using this QuerySet, make sure the model inherits from core.models.AbstractBaseModel
    """
    def deleted(self, *args, **kwargs):
        """
        Filter objects that are marked as deleted.
        """
        return self.filter(is_deleted=True, *args, **kwargs)
    
    def non_deleted(self, *args, **kwargs):
        """
        Filter objects that are not marked as deleted.
        """
        return self.filter(is_deleted=False, *args, **kwargs)
    
    def today(self, *args, **kwargs):
        """
        Filter objects created today.
        """
        today = timezone.now().date()
        return self.filter(created_on__date=today, *args, **kwargs)
    
    def yesterday(self, *args, **kwargs):
        """
        Filter objects created yesterday.
        """
        yesterday = timezone.now().date() - timezone.timedelta(days=1)
        return self.filter(created_on__date=yesterday, *args, **kwargs)



class BaseAbstractManager(models.Manager.from_queryset(BaseAbstractQuerySet)):
    """
    Base manager for all models.
    Inherit all queryset methods automatically.
    """
    pass
