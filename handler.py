import inspect
from typing import Callable, Any, Dict, Type

class ChaosHandler:
    def __init__(self):
        self._strategies: Dict[Type[BaseException], Callable] = {}

    def register(self, exception_cls: Type[BaseException]):
        def decorator(func: Callable):
            self._strategies[exception_cls] = func
            return func
        return decorator

    def handle(self, target_func: Callable):
        def wrapper(*args, **kwargs):
            try:
                return target_func(*args, **kwargs)
            except Exception as e:
                exc_type = type(e)
                handler = next((self._strategies[t] for t in self._strategies if issubclass(exc_type, t)), None)
                if not handler:
                    raise e
                
                sig = inspect.signature(handler)
                params = list(sig.parameters.keys())
                recovery_data = {
                    'exception': e,
                    'func': target_func,
                    'args': args,
                    'kwargs': kwargs
                }
                pass_args = {k: v for k, v in recovery_data.items() if k in params}
                if len(pass_args) < len(params):
                    return handler()
                return handler(**pass_args)
        return wrapper

chaos_healer = ChaosHandler()

@chaos_healer.register(ZeroDivisionError)
def handle_zero_division():
    return float('inf')

@chaos_healer.register(TypeError)
def handle_type_error(exception, func, args, kwargs):
    sig = inspect.signature(func)
    param_names = list(sig.parameters.keys())
    if not param_names or not args:
        raise exception
    try:
        if isinstance(args[0], str):
            healed_args = (float(args[0]),) + args[1:]
            return func(*healed_args, **kwargs)
    except (ValueError, TypeError):
        pass
    raise exception