import logging
from typing import Optional
from contextvars import ContextVar


logger = logging.getLogger(__name__)
_current_user: ContextVar[Optional["User"]] = ContextVar("current_user", default=None) # type: ignore


class ThreadLocalUser:
    """
    Thread-local storage for the current user.
    """
    
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def set_current_user(user) -> None:
        _current_user.set(user)
        logger.debug
    
    @staticmethod
    def get_current_user():
        user = _current_user.get()
        logger.debug(f"Got user from context: {user}")
        return user
    
    @staticmethod
    def clear_current_user() -> None:
        _current_user.set(None)







class CurrentThreadUserMiddleware:
    """
    Middleware to save the current user in thread-local storage.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.thread = ThreadLocalUser()
    
    def __call__(self, request):
        # Set the current user before proceeding to the request
        self.thread.set_current_user(getattr(request, "user", None))
        
        response = None
        
        try:
            response = self.get_response(request)
        except Exception as e:
            logger.error(f"Error processing request: {e}", exc_info=True)
        finally:
            # Clear the user after the request
            self.thread.clear_current_user()
        
        if response:
            return response
        
        logger.warning("No response was returned by the view.")
        raise ValueError(f"{self.__class__.__name__} failed to get a valid response.")
