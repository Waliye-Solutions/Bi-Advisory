from django import forms
from contacts.models import Contact
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["full_name", "phone_number", "email", "subject", "message"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control mb-4", "placeholder": _("Nom & Prénom")}),
            "phone_number": forms.TextInput(attrs={"class": "form-control mb-4", "placeholder": _("Téléphone"), "minlength": 8,}),
            "email": forms.EmailInput(attrs={"class": "form-control mb-4", "autocomplete": "email", "placeholder": _("Email")}),
            "subject": forms.TextInput(attrs={"class": "form-control mb-4", "placeholder": _("Sujet")}),
            "message": forms.Textarea(attrs={"class": "form-control mb-4", "rows": 5, "placeholder": _("Votre message")}),
        }
