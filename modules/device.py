# Мне лень доделывать
from pyrogram import Client, filters
import platform
import psutil
import os
import subprocess

@Client.on_message(filters.command("matefetch", prefixes=".") & filters.me)
async def device_handler(client, message):
    try:
        os_name = platform.freedesktop_os_release().get('PRETTY_NAME')
    except:
        os_name = platform.system() 

    await message.edit(f"**ОС: ** __{os_name}__")
