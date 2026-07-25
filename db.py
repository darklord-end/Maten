import json
import threading
import logging

__all__ = ["Database"]

_logger = logging.getLogger(__name__)
_db_lock = threading.Lock()
_db_instance = None

class Database:
    db = {}

    def __new__(cls):
        global _db_instance
        if _db_instance is None:
            _db_instance = super().__new__(cls)
            _db_instance._initialized = False
            _db_instance._dirty = False
            _db_instance._timer = None
        return _db_instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.load()
        self._schedule_save()

    def load(self):
        try:
            with _db_lock:
                with open("database.json", "r") as f:
                    Database.db = json.load(f)
        except FileNotFoundError:
            Database.db = {}

    def set(self, owner, key, value):
        with _db_lock:
            if owner not in Database.db:
                Database.db[owner] = {}
            Database.db[owner][key] = value
            self._dirty = True

    def get(self, owner, key):
        with _db_lock:
            if owner in Database.db and key in Database.db[owner]:
                return Database.db[owner][key]
            return None

    def _schedule_save(self):
        if self._timer is not None:
            self._timer.cancel()
        self._timer = threading.Timer(3.0, self._flush)
        self._timer.daemon = True
        self._timer.start()

    def _flush(self):
        if not self._dirty:
            self._schedule_save()
            return
        with _db_lock:
            try:
                with open("database.json", "w") as f:
                    json.dump(Database.db, f, indent=4, ensure_ascii=False)
                self._dirty = False
            except OSError as e:
                _logger.error("Failed to flush database: %s", e)
        self._schedule_save()

    def save(self):
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None
        with _db_lock:
            try:
                with open("database.json", "w") as f:
                    json.dump(Database.db, f, indent=4, ensure_ascii=False)
                self._dirty = False
            except OSError as e:
                _logger.error("Failed to save database: %s", e)