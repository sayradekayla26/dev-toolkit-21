import sys
from typing import Callable, Any, Tuple

class FastRegisterCache:
    """
    A creative dual-register L1/L2 cache decorator for high-frequency operations.
    Bypasses standard dict hash lookups for consecutive identical arguments
    by storing them in fast-access local slot variables (registers).
    """
    def __init__(self, func: Callable[..., Any]):
        self.func = func
        self.r1_key: Tuple[Any, ...] = ()
        self.r1_val: Any = None
        self.r1_active = False
        self.l2_space = type("L2Space", (), {})()

    def __call__(self, *args: Any) -> Any:
        if self.r1_active and self.r1_key == args:
            return self.r1_val

        attr_key = sys.intern(f"c_{hash(args)}")
        try:
            res = getattr(self.l2_space, attr_key)
            self.r1_key = args
            self.r1_val = res
            self.r1_active = True
            return res
        except AttributeError:
            pass

        result = self.func(*args)
        setattr(self.l2_space, attr_key, result)
        
        self.r1_key = args
        self.r1_val = result
        self.r1_active = True
        return result

    def invalidate(self) -> None:
        self.r1_active = False
        self.r1_val = None
        self.r1_key = ()
        self.l2_space = type("L2Space", (), {})()
