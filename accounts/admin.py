from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.admin import GroupAdmin as DjangoGroupAdmin, UserAdmin as _UserAdmin

from accounts.models import User
from utilities.mixins.admins import AbstractBaseModelAdmin, CustomModelExemptedAdmin


class UserAdmin(_UserAdmin, AbstractBaseModelAdmin): # type: ignore
    list_display = ["email", "username", "is_active", "date_joined"]
    search_fields = (
        "email", "username", "phone_number", "first_name", "last_name", "username",
        "last_login", "is_active", "is_staff", "is_superuser", "date_of_birth", "bio",
        *AbstractBaseModelAdmin.search_fields
    )
    list_filter = ("is_active", "is_staff", "is_superuser", "date_joined", *AbstractBaseModelAdmin.list_filter)
    date_hierarchy = "date_joined"
    readonly_fields = (
        "date_joined", "last_login",
        "username", "email",
        *_UserAdmin.readonly_fields, *AbstractBaseModelAdmin.readonly_fields
    )
    filter_horizontal = ("groups",  *_UserAdmin.filter_horizontal, *AbstractBaseModelAdmin.filter_horizontal)
    fieldsets = None # type: ignore # reset default fieldsets and use Django default fieldsets (instead of custom ones from AbstractBaseModelAdmin)


class CustomGroupAdmin(DjangoGroupAdmin, CustomModelExemptedAdmin):
    pass



# unregister default Group model
admin.site.unregister(DjangoGroup)

admin.site.register(User, UserAdmin)
# admin.site.register(DjangoGroup, CustomGroupAdmin)
