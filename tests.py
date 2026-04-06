# requires: requests, psutil
# Этот модуль проверяет защиту Maten

from pyrogram import Client, filters
import requests
import os
# -------------------------------------------------
@Client.on_message(filters.command("try_join", prefixes=".") & filters.me)
async def try_join_handler(client, message):
    # Проверка защиты от авто-подписки
    await message.edit("Попытка войти в канал @telegram...")
    try:
        # Твой перехваченный метод app.join_chat должен это заблокировать
        await client.join_chat("mikhaylodm")
        await message.edit("⚠️ Ой, я смог подписаться! Защита не сработала.")
    except Exception as e:
        await message.edit(f"🛡️ Защита сработала: {e}")