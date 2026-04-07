from pyrogram import Client, filters
import os

class Modules:
    @staticmethod
    def register_handlers(app):
        @app.on_message(filters.command("modules", prefixes=".") & filters.me)
        async def modules_handler(client, message):
            modules = os.listdir("modules")
            await message.edit("Модули: " + ", ".join(modules))

