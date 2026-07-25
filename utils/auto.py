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

        limit_reached = False
        token = None
        try:
            async for message in app.get_chat_history(bot_father, limit=5):
                if not message.text:
                    continue
                if "Sorry, you can't add more" in message.text:
                    limit_reached = True
                    break
                match = re.search(r"(\d{8,10}:[A-Za-z0-9_-]{35})", message.text)
                if match:
                    token = match.group(1)
                    break
        except TypeError as e:
            if "'NoneType' object is not iterable" in str(e):
                print("[!] Не удалось получить историю чата с BotFather.")
                return
            raise

        if limit_reached:
            print("[!] Достигнут лимит ботов (максимум 20). Удалите старые боты или передайте управление.")
            return

        if not token:
            print("[!] Не удалось получить токен от BotFather.")
            return

        db.set("system", "bot_token", token)
        db.set("system", "bot_username", username)
        print(f"Бот: @{username}")

        await app.send_message(username, "/start")

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

    except Exception as e:
        print(f"[!!!] Ошибка: {e}")
