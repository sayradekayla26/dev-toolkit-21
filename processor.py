import time
import random
from typing import Iterator, Type, Tuple, Union

class Attempt:
    def __init__(self, retrier: "RetryLoop"):
        self.retrier = retrier

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.retrier.stop()
            return True
        if issubclass(exc_type, self.retrier.exceptions):
            self.retrier.handle_failure(exc_val)
            return True
        return False

class RetryLoop:
    def __init__(
        self,
        max_attempts: int = 3,
        delay: float = 0.1,
        backoff: float = 2.0,
        exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception,
    ):
        self.max_attempts = max_attempts
        self.delay = delay
        self.backoff = backoff
        self.exceptions = exceptions
        self._current_attempt = 0
        self._running = True

    def __iter__(self) -> Iterator[Attempt]:
        self._current_attempt = 0
        self._running = True
        while self._current_attempt < self.max_attempts and self._running:
            self._current_attempt += 1
            yield Attempt(self)
            if not self._running:
                break
            if self._current_attempt < self.max_attempts:
                sleep_time = self.delay * (self.backoff ** (self._current_attempt - 1))
                sleep_time += random.uniform(0, 0.1 * sleep_time)
                time.sleep(sleep_time)

    def stop(self):
        self._running = False

    def handle_failure(self, exc: Exception):
        if self._current_attempt >= self.max_attempts:
            raise exc