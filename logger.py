from datetime import datetime
from threading import Lock


class Logger:
    _lock: Lock

    def __init__(self):
        self._lock = Lock()

    def log(self, msg: str):
        with self._lock:
            print(f'[{datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")}] {msg}')
