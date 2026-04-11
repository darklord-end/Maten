import time
import psutil
import platform
import sys
import os
from pyrogram import Client, filters
from datetime import datetime
from git import Repo 

start_time = time.time()

class Info:
    @staticmethod
    def register_handlers(app, prefix):
        @app.on_message(filters.command("info", prefixes=prefix) & filters.me)
        async def information_handler(client, message):
            try:
                repo = Repo('.')
                head = repo.head.commit
                commit_hash = head.hexsha[:7]
            except Exception:
                commit_hash = "unknown"

            uptime_seconds = int(time.time() - start_time)
            uptime = str(datetime.utcfromtimestamp(uptime_seconds).strftime('%H:%M:%S'))
            
            cpu_usage = psutil.cpu_percent()
            ram = psutil.virtual_memory()
            ram_usage = f"{ram.used // (1024**2)} MB / {ram.total // (1024**2)} MB"
            
            pyro_version = "2.3.69" # Pyrofork
            
            photo_url = "https://github.com/darklord-end/Imagessss/blob/main/Info.png?raw=true"
            
            caption = (
                f"🔍 **Maten Userbot** `#{commit_hash}`\n"
                f"───\n"
                f"📂 **Core:** `Pyrofork {pyro_version}`\n"
                f"🐍 **Python:** `{platform.python_version()}`\n"
                f"───\n"
                f"👤 **Owner:** {(await client.get_me()).first_name}\n"
                f"⌨️ **Prefix:** `{prefix}`\n"
                f"⌛️ **Uptime:** `{uptime}`\n"
                f"───\n"
                f"⚡️ **CPU:** `{cpu_usage}%`\n"
                f"💼 **RAM:** `{ram_usage}`\n"
                f"🐧 **OS:** `{platform.system()}`\n"
                f"───\n"
                f"📦 **Repo:** [GitHub](https://github.com/darklord-end/Maten)"
            )

            await message.delete()
            await client.send_photo(
                chat_id=message.chat.id,
                photo=photo_url,
                caption=caption
            )
