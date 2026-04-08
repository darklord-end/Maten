# Инфо TODO
from pyrogram import Client, filters
from utils import *

class Info:
    @staticmethod
    def register_handlers(app, prefix):
        @app.on_message(filters.command("info", prefixes=prefix) & filters.me)
        async def information_handler(client, message):
            photo_url = "https://github.com/darklord-end/Maten/blob/main/images/Info.png?raw=true" 
            #TODO - MOVE TO OTHER REPO!
            await message.delete()
            
            await client.send_photo(
                chat_id=message.chat.id,
                photo=photo_url,
                caption="**Инфо:**\nMaten\nПлатформа: " + get_platform()
            )

        # Help TODO
        @app.on_message(filters.command("help", prefixes=".") & filters.me)
        async def help_handler(client, message):
            await message.edit("Заглушка")