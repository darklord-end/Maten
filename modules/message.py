# ПРОСТО БАЗА
from pyrogram import Client, filters

class Message:
    @staticmethod
    def register_handlers(app, prefix):
            @app.on_message(filters.command("message", prefixes=prefix) & filters.me)
            async def message_aaa(client, message):
                await message.edit("Тест команда!")
                await client.send_message("me", "Тест команда!")

message_instance = Message()
