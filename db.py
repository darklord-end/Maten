import json
import asyncio

__all__ = ["Database"]

class Database:
    db = {}
    
    def __init__(self):
        self.load()
    
    def load(self):
        try:
            with open("database.json", "r") as f:
                Database.db = json.load(f)
        except FileNotFoundError:
            Database.db = {}
    
    def set(self, owner, key, value):
        if owner not in Database.db:
            Database.db[owner] = {}
        Database.db[owner][key] = value
        self.save()
    
    def get(self, owner, key):
        if owner in Database.db and key in Database.db[owner]:
            return Database.db[owner][key]
        return None
    
    def save(self):
        with open("database.json", "w") as f:
            json.dump(Database.db, f, indent=4, ensure_ascii=False)