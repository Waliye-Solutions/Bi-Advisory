import random, string
from django.apps import apps
from email.headerregistry import Address



class AccountUtils:
    
    @staticmethod
    def get_username_from_email(email: str, force_integrity: bool = True) -> str:
        """Generate username from a given email address
        
        Args:
            email (str): Email address
            force_integrity (bool): if `True` then force username by appending additional chars
        
        Returns:
            str: Username in alpha numeric format
        """
        base_username = "".join(filter(str.isalnum, Address(addr_spec=email).username)).strip().lower()
        
        # if integrity is not forced, return the base username without checking for duplicates
        if not force_integrity:
            return base_username
        
        # Ensure the generated username is unique by appending random characters if necessary
        UserModel = apps.get_model(app_label="accounts", model_name="User")
        username = base_username
        while UserModel.objects.filter(username=username).exists():
            chars = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
            username = f"{base_username}{chars}"
        
        return username.strip().lower()
