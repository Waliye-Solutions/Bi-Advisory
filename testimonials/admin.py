from django.contrib import admin

from testimonials.models import Testimonial
from utilities.mixins.admins import AbstractBaseModelAdmin


class TestimonialAdmin(AbstractBaseModelAdmin):
    list_display = ("client_name", "client_position", "client_country", "stars", *AbstractBaseModelAdmin.list_display)
    search_fields = (*AbstractBaseModelAdmin.search_fields, "client_name", "client_position", "client_country", "feedback")
    list_filter = (*AbstractBaseModelAdmin.list_filter, "stars")


admin.site.register(Testimonial, TestimonialAdmin)
