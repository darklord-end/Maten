# Инфо TODO
from pyrogram import Client, filters
from utils import *

class Info:
    @staticmethod
    def register_handlers(app, prefix):
        @app.on_message(filters.command("info", prefixes=prefix) & filters.me)
        async def information_handler(client, message):
            photo_url = "https://github.com/darklord-end/Imagessss/blob/main/Info.png?raw=true" 
            await message.delete()
            
            await client.send_photo(
                chat_id=message.chat.id,
                photo=photo_url,
                caption="🔍**Maten** "
                "\n"
            )

        # Help TODO
        @app.on_message(filters.command("help", prefixes=".") & filters.me)
        async def help_handler(client, message):
            await message.edit("Заглушка")