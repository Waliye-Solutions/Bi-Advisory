from django.contrib import admin

from newsletter.models import Newsletter
from utilities.mixins.admins import AbstractBaseModelAdmin


class NewsletterAdmin(AbstractBaseModelAdmin):
    list_display = ("email", "is_subscribed", *AbstractBaseModelAdmin.list_display)
    search_fields = (*AbstractBaseModelAdmin.search_fields, "email", "is_subscribed")
    list_filter = ("is_subscribed", *AbstractBaseModelAdmin.list_filter,)


admin.site.register(Newsletter, NewsletterAdmin)
