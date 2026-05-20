import time
from functools import wraps
from typing import Callable, Any

def rate_limit(max_per_second: float) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to limit how often a function can be executed.
    
    Args:
        max_per_second: The maximum number of allowed calls per second.
    """
    min_interval = 1.0 / max_per_second
    last_called = 0.0

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal last_called
            now = time.time()
            elapsed = now - last_called
            
            # If the function is called too soon, calculate how long to sleep
            if elapsed < min_interval:
                time_to_wait = min_interval - elapsed
                time.sleep(time_to_wait)
            
            # Update the last called timestamp *after* any potential sleep
            last_called = time.time()
            return func(*args, **kwargs)
            
        return wrapper
    return decorator