import time
from functools import wraps

def rate_limit(calls_per_minute: int):
    """Decorator to limit function calls to a set number per minute."""
    interval = 60.0 / calls_per_minute
    def decorator(func):
        last_call = [0]
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < interval:
                time.sleep(interval - elapsed)
            result = func(*args, **kwargs)
            last_call[0] = time.time()
            return result
        return wrapper
    return decorator