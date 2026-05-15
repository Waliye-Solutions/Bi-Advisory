from django.contrib import admin

from contacts.models import Contact
from utilities.mixins.admins import AbstractBaseModelAdmin


class ContactAdmin(AbstractBaseModelAdmin):
    list_display = ("full_name", "email", "phone_number", "subject", *AbstractBaseModelAdmin.list_display)
    search_fields = (*AbstractBaseModelAdmin.search_fields, "full_name", "email", "phone_number", "subject", "message")
    list_filter = (*AbstractBaseModelAdmin.list_filter,)


admin.site.register(Contact, ContactAdmin)
