# Добавить туда ещё функции наверн
from pyrogram import Client, filters
import os, sys, time

@Client.on_message(filters.command("restart", prefixes=".") & filters.me)
async def restart_handler(client, message):
    await message.edit("Перезагружаю Maten...")
    time.sleep(1)
    os.execl(sys.executable, sys.executable, *sys.argv)  


@Client.on_message(filters.command("shutdown", prefixes=".") & filters.me)
async def shutdown_handler(client, message):
    await message.edit("Завершаю Maten...")
    time.sleep(1)
    sys.exit()