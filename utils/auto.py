import asyncio
import random
import string
import re
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from db import Database

db = Database()

async def start_automation(app: Client):
    print("[*] Начинаю автоматизацию создания бота...")
    bot_father = "BotFather"
    display_name = "Maten"
    rand_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    username = f"maten_{rand_str}_bot"
    
    pic_url = "https://github.com/darklord-end/Imagessss/blob/main/Logo2.png?raw=true"

    async def send_with_delay(text, delay=2):
        try:
            await app.send_message(bot_father, text)
            await asyncio.sleep(delay)
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
            await app.send_message(bot_father, text)

    try:
        await send_with_delay("/newbot")
        await send_with_delay(display_name)
        await send_with_delay(username, delay=3)

        await send_with_delay("/setuserpic")
        await send_with_delay(f"@{username}")
        try:
            await app.send_photo(bot_father, pic_url)
            await asyncio.sleep(2)
        except Exception as e:
            print(f"[!] Не удалось установить фото: {e}")

        await send_with_delay("/setinline")
        await send_with_delay(f"@{username}")
        await send_with_delay("Maten...")

        token = None
        async for message in app.get_chat_history(bot_father, limit=15):
            if message.text:
                match = re.search(r"(\d{8,10}:[A-Za-z0-9_-]{35})", message.text)
                if match:
                    token = match.group(1)
                    break

        if token:
            db.set("system", "bot_token", token)
            db.set("system", "bot_username", username)
            print(f"Бот: @{username}")
            
            await app.send_message(username, "/start")
        else:
            print("[!] Токен не найден.")

    except Exception as e:
        print(f"[!!!] Ошибка: {e}")
