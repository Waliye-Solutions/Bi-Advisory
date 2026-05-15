from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from contacts.forms import ContactForm


def contact_view(request):
    form = ContactForm()
    
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # No need special valadation, just saving the contact, the email will be sent in background by the task
            contact = form.save()
            messages.success(request, _("Message envoyé avec succès. Nous vous contacterons bientôt."))
            return redirect(".")
        
        else:  # if not form.is_valid()
            errors = form.errors.as_data()
            for error in errors:
                msg = str(errors[error][0].message)
                messages.error(request, _(f"{msg}"))
            return redirect(".")
    
    context = {
        "form": form,
        "contact_page_is_active": True,
    }
    template_name = "contacts/contact.html"
    return render(request, template_name,  context)
