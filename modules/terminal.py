#Терминал
from pyrogram import Client, filters
import subprocess

class Terminal:
    @staticmethod
    def register_handlers(app, prefix):
        @app.on_message(filters.command("terminal", prefixes=prefix) & filters.me)
        async def terminal(client, message):
            cmd = message.text.split(None, 1)[1]
            result = subprocess.getoutput(cmd)
            await message.edit("Команда: " + cmd + "\nРезультат: " + result + "\n")
