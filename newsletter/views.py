from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from newsletter.models import Newsletter

def subscribe_newsletter_view(request):
    _HTTP_REFERER = request.META.get("HTTP_REFERER", "/")
    
    if request.method == "POST":
        email = request.POST.get("email")
        if email and isinstance(email, str):
            Newsletter.objects.create(email=email, is_subscribed=True)
            messages.success(request, _("Merci de vous être abonné à notre newsletter !"))
        else:
            messages.error(request, _("Veuillez fournir une adresse e-mail valide."))
    return redirect(_HTTP_REFERER)
