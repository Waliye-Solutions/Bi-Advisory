from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class TestimonialsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'testimonials'
    verbose_name = _("Avis & Retours clients")
