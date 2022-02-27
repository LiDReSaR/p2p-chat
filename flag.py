from threading import Lock


class Flag:
    _value: bool
    _lock: Lock

    def __init__(self) -> None:
        self._value = False
        self._lock = Lock()

    def get(self) -> bool:
        with self._lock:
            return self._value

    def set(self, value: bool) -> None:
        with self._lock:
            self._value = value
