import ssl
import logging
from typing import List, Optional

from django.conf import settings
from django.http import HttpRequest
from django.utils.functional import cached_property
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMessage, get_connection
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend


logger = logging.getLogger(__name__)



class DevEmailBackend(SMTPBackend):
    """
    Email backend to use (only) in dev mode (it doesn't check hostname while creating connection).
    While being in dev mode Django doesn't allow email sending directly to email address (only console backend works).
    To override this and to be able to send actual email in dev mode, use this as email backend.
    
    Args:
        SMTPBackend (_type_): A wrapper that manages the SMTP network connection.
    
    Returns:
        SSLContext: SSLContext instance
    """
    @cached_property
    def ssl_context(self) -> ssl.SSLContext:
        if self.ssl_certfile or self.ssl_keyfile:
            ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
            ssl_context.load_cert_chain(self.ssl_certfile, self.ssl_keyfile) # type: ignore
            return ssl_context
        
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        return ssl_context




class BaseEmailService:
    """
    Base email service to be inherited by other email services.
    """
    
    def __init__(
        self,
        mail_subject: str,
        email_content: str,
        receivers: List[str],
        context: Optional[dict] = None,
        request: Optional[HttpRequest] = None,
    ) -> None:
        
        self.request = request
        self.mail_subject = mail_subject
        self.email_content = email_content
        self.receivers = receivers
        self.context = context or {}
        self.context.update({
            "mail_subject": self.mail_subject,
            "site_name": settings.SITE_NAME,
            "site_phone_number": settings.SITE_PHONE_NUMBER,
            "site_email_address": settings.SITE_EMAIL_ADDRESS,
        })
    
    
    
    def _build_email_message(
        self, from_email: str, connection: BaseEmailBackend | None = None
    ) -> EmailMessage:
        email = EmailMessage(
            subject=self.mail_subject,
            body=self.email_content,
            from_email=from_email,
            to=self.receivers,
            connection=connection,
        )
        email.content_subtype = "html" # to send email as HTML (if the content is in HTML format)
        return email
    
    
    def _get_custom_connection(self, from_email_address: str, password: str) -> BaseEmailBackend:
        """ Send email with custom connection (not using default email)
        
        Args:
            from_email_address (str): Email address to use for this custom connection
            password (str): Password of the email address to use for this custom connection
        
        Returns:
            _type_: _description_
        """
        return get_connection(
            backend=settings.EMAIL_BACKEND,
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=from_email_address,
            password=password,
            use_tls=settings.EMAIL_USE_TLS,
        )
    
    def send(self, from_email: Optional[str] = None) -> str:
        """ Send email to users using default connection (using default email address and password defined in settings) """
        from_email = from_email or str(settings.DEFAULT_FROM_EMAIL)
        email = self._build_email_message(from_email=from_email)
        
        try:
            email.send()
            logger.info("Email sent to %s (subject : %s)", self.receivers, self.mail_subject)
            return str(_("Email sent successfully !"))
        except Exception:
            logger.exception(
                "Failed to send email to %s (subject : %s)",
                self.receivers,
                self.mail_subject,
            )
            raise
    
    
    def send_with_custom_connection(self, from_email_address: str, password: str) -> str:
        connection = self._get_custom_connection(from_email_address, password)
        email = self._build_email_message(from_email=from_email_address, connection=connection)
        
        try:
            email.send()
            logger.info("Email sent (custom) to %s from %s", self.receivers, from_email_address)
            return str(_("Email sent successfully !"))
        except Exception:
            logger.exception("Failed to send email (custom) to %s from %s", self.receivers, from_email_address)
            raise





class TemplateEmailService(BaseEmailService):
    """
    Send email using a Django template.
    
    Example:
        service = TemplateEmailService(
            mail_subject="Bienvenue",
            mail_template="emails/welcome.html",
            receivers=["user@example.com"],
            context={"user": user},
        )
        service.send()
    """
    
    def __init__(
        self,
        mail_subject: str,
        mail_template: str,
        receivers: List[str],
        context: Optional[dict] = None,
        request: Optional[HttpRequest] = None,
    ) -> None:
        
        context = context or {}
        context.update({
            "mail_subject": mail_subject,
            "site_name": settings.SITE_NAME,
            "site_phone_number": settings.SITE_PHONE_NUMBER,
            "site_email_address": settings.SITE_EMAIL_ADDRESS,
        })
        
        email_content = render_to_string(mail_template, context, request=request)
        
        super().__init__(
            mail_subject=mail_subject,
            email_content=email_content,
            receivers=receivers,
            context=context,
            request=request,
        )
        self.mail_template = mail_template




class RawEmailService(BaseEmailService):
    """
    Use this service to send an email with raw HTML/plain text content, without using a Django template.
    Useful for simple notifications or dynamically generated emails.
    """
    # This service is essentially the same as BaseEmailService, but it exists to clarify the intention in the calling code.
