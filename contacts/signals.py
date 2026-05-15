from django.dispatch import receiver
from django.db.models.signals import post_save

from contacts.models import Contact
from contacts.tasks import send_contact_email


@receiver(post_save, sender=Contact)
def on_contact_created(sender, instance: Contact, created: bool, **kwargs) -> None:
    """
    Signal handler for Contact model's post_save signal. It sends an email to the admin (contact email) when a new contact is created.
    """
    if created:
        send_contact_email.after_response(instance.pk) # type: ignore
