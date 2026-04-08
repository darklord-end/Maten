# Инфо TODO
from pyrogram import Client, filters

class Info:
    @staticmethod
    def register_handlers(app, prefix):
        @app.on_message(filters.command("info", prefixes=prefix) & filters.me)
        async def information_handler(client, message):
            photo_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3DS4NNjOyOHSXCO5WeN7FWaf6vrpWE1mhKw&s" 
            
            await message.delete()
            
            await client.send_photo(
                chat_id=message.chat.id,
                photo=photo_url,
                caption="**Инфо:**\n Maten"
            )

        # Help TODO
        @app.on_message(filters.command("help", prefixes=".") & filters.me)
        async def help_handler(client, message):
            await message.edit("Заглушка")