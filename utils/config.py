from db import Database

db = Database()

class Config:
    @property
    def prefix(self) -> str:
        pref = db.get("main", "prefix")
        
        if pref is None:
            default = "."
            db.set("main", "prefix", default)
            return default
            
        return pref

    def set_prefix(self, new_prefix: str):
        db.set("main", "prefix", new_prefix)

config = Config()