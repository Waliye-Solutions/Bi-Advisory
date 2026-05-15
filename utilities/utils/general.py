from typing import Optional, Union
import json, re, hmac, hashlib, logging

from django.apps import apps
from pygments import highlight
from django.conf import settings
from django.utils import timezone
from django.http import HttpRequest
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
from django.utils.safestring import mark_safe

IP_RE = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
logger = logging.getLogger(__name__)


class BaseUtils:
    
    @staticmethod
    def prettify_json_data(
        data: Optional[dict] = None, sort: Optional[bool] = False, sort_key: Optional[str] = None) -> Union[dict, str]:
        if not data or data is None:
            return {}
        
        sorted_data = data
        if sort and sort_key:
            try:
                sorted_data = sorted(data, key=lambda x: x.get(sort_key, ""), reverse=True)
            except Exception as e:
                sorted_data = list(reversed(data))
        
        try:
            raw_json = json.dumps(sorted_data, indent=4, ensure_ascii=False)
            formatter = HtmlFormatter(style="colorful", full=False, noclasses=True)
            highlighted_json = highlight(raw_json, JsonLexer(), formatter)
            
            styled_block = f"""
                <div style="max-height: 400px; overflow-y: auto; background: #f8f8f8; padding: 10px; border: 1px solid #ddd; font-family: monospace; font-size: 14px;">
                    {highlighted_json}
                </div>
            """
            
            return mark_safe(styled_block)
        except Exception as e:
            return {}
    
    
    @staticmethod
    def get_client_ip(request: HttpRequest):
        """
        Retrieves the remote IP address from the request data.
        **NOTE** This function was taken from django-tracking (MIT LICENSE)
        
        Args:
            request (HttpRequest): The HTTP request object.
        
        Returns:
            str: The client's IP address.
        """
        ip_address = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", "127.0.0.1"))
        if ip_address:
            # make sure we have one and only one IP
            try:
                ip_address = IP_RE.match(ip_address)
                if ip_address:
                    ip_address = ip_address.group(0)
                else:
                    # no IP, probably from some dirty proxy or other device
                    # throw in some bogus IP
                    ip_address = "10.0.0.1"
            except IndexError:
                pass
        return ip_address
    
    
    @staticmethod
    def verify_device_signature(payload, signature):
        """
        Verify the HMAC signature of a device 
        
        Args:
            payload: Data
            signature: Device signature
        
        Returns:
            bool: if access to the device is granted or not
        """
        if not signature:
            return False
        
        expected_signature = hmac.new(
            settings.DEVICE_WEBHOOK_SECRET.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, f"sha256={expected_signature}")
    
    
    @staticmethod
    def format_historical_data_to_store_as_copy(action: Optional[str] = None, current_user=None, data=None):
        UserModel = apps.get_model("accounts", "User")
        
        try:
            serialized_data = json.dumps(data)
        except Exception as e:
            serialized_data = None
            error = f"Can't convert data to JSON: {e}"
            logger.error(error, exc_info=True)
            return None
        
        data_to_save = {
            "timestamp": timezone.now().isoformat(),
            "data": serialized_data,
        }
        if action:
            data_to_save.update({"action": str(action)})
        
        if isinstance(current_user, UserModel):
            data_to_save.update({
                "user_id": current_user.pk,
                "user_username": getattr(current_user, "username", ""),
                "user_full_name": getattr(current_user, "full_name", ""),
            })
        return data_to_save
