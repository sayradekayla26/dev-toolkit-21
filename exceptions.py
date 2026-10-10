class ToolkitBaseError(Exception):
    def __init__(self, message, code=500):
        self.code = code
        super().__init__(f'[{code}] {message}')

class ConfigurationError(ToolkitBaseError):
    pass

class ResourceExhaustedError(ToolkitBaseError):
    pass

class ProcessingFailure(ToolkitBaseError):
    pass

def raise_if_none(value, message, exc_class=ToolkitBaseError):
    if value is None:
        raise exc_class(message)
    return value

class ExceptionDispatcher:
    def __init__(self):
        self._handlers = {}

    def register(self, exc_type, handler):
        self._handlers[exc_type] = handler

    def handle(self, exc):
        handler = self._handlers.get(type(exc), self._default_handler)
        return handler(exc)

    @staticmethod
    def _default_handler(exc):
        print(f'Critical system trace: {exc}')
        raise exc

if __name__ == '__main__':
    dispatcher = ExceptionDispatcher()
    dispatcher.register(ConfigurationError, lambda e: print(f'Config fix required: {e}'))