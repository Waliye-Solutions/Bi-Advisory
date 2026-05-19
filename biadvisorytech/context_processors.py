from django.conf import settings

def global_context(request):
    context = {
        "site_name": getattr(settings, "SITE_NAME", "Bi Advisory"),
        "site_phone_number": getattr(settings, "SITE_PHONE_NUMBER", "+225 01 01 07 60 29"),
        "site_email_address": getattr(settings, "SITE_EMAIL_ADDRESS", "contact@biadvisorytech.com"),
        "site_description": getattr(settings, "SITE_DESCRIPTION", ""),
        "site_address": getattr(settings, "SITE_ADDRESS", "Abidjan, Côte d'Ivoire"),
    }
    return context
