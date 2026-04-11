from db import Database

db = Database()

def get_owner_id():
    return db.get("system", "owner_id")

def is_owner(user_id):
    owner_id = get_owner_id()
    # Если в базе пусто, на всякий случай пропускаем (или заполни при старте)
    if not owner_id:
        return False
    return int(owner_id) == int(user_id)

async def set_owner_id(client):
    me = await client.get_me()
    db.set("system", "owner_id", me.id)
    print(f"[*] ID владельца {me.id} сохранен.")