from pyrogram import Client, errors
import time, asyncio, sys
#import logging

#logging.basicConfig(level=logging.INFO)

app = Client("my_account", plugins=dict(root="modules"))
app.pending_pkg = {} 

# ПЕРЕПИСАТЬ (ИИ-СЛОП)

original_join = app.join_chat

async def protected_join(chat_id):
    print(f"[-] Блокировка попытки входа в канал: {chat_id}")
    return None

app.join_chat = protected_join 

async def safe_edit(message, text):
    try:
        await message.edit(text)
        await asyncio.sleep(0.3) # Защитная пауза между действиями
    except Exception as e:
        print(f"[!] Ошибка флуда: {e}")


print("[+] Maten запущен...")

app.run()