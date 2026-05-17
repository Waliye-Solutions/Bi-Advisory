from django.contrib import admin

from teams.models import Team
from utilities.mixins.admins import AbstractBaseModelAdmin


class TeamAdmin(AbstractBaseModelAdmin):
    list_display = ("full_name", "role", *AbstractBaseModelAdmin.list_display)
    search_fields = ("full_name", "role", "facebook", "twitter", "linkedin", "instagram", *AbstractBaseModelAdmin.search_fields)


admin.site.register(Team, TeamAdmin)
