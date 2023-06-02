import threading


class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance


class Logger(Singleton):
    def __init__(self):
        self.file = open("log.txt", "w", encoding="utf-8")

    def log(self, message):
        self.file.write(f"{message}"+ "\n")
        self.file.flush()
