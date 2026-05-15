from django.contrib import admin

from services.models import Service
from utilities.mixins.admins import AbstractBaseModelAdmin


class ServiceAdmin(AbstractBaseModelAdmin):
    list_display = ("name", "summary", *AbstractBaseModelAdmin.list_display)
    search_fields = (*AbstractBaseModelAdmin.search_fields, "name", "summary", "description")
    list_filter = (*AbstractBaseModelAdmin.list_filter,)


admin.site.register(Service, ServiceAdmin)
