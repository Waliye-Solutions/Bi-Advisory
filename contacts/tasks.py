import logging
import after_response

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from biadvisorytech.services.email import TemplateEmailService


logger = logging.getLogger(__name__)



@after_response.enable
def send_contact_email(contact_id):
    from contacts.models import Contact
    
    try:
        contact = Contact.objects.get(pk=contact_id)
    except Contact.DoesNotExist:
        logger.error("send_contact_email : unable to find contact/message with id %s, email not sent", contact_id)
        return
    
    try:
        email_template = "public/emails/contact.html"
        email = TemplateEmailService(
            mail_subject=str(_(f"Nouveau message sur le site : {contact.subject}")),
            mail_template=email_template,
            receivers=settings.DEFAULT_EMAIL_RECIPIENTS,
            context={"contact": contact},
        )
        output = email.send()
        logger.info("send_contact_email : email sent for contact (id=%s).", contact_id)
        return output
    except Exception:
        logger.exception("send_contact_email : failed to send email for contact (id=%s).", contact_id, exc_info=True)
