from pyrogram import Client, filters
from aiogram import types
import random

class Testinline:
    @staticmethod
    def register_handlers(app, prefix):
        @app.on_message(filters.command("test", prefixes=prefix) & filters.me)
        async def test_cmd(client, message):
            from utils import db
            bot_username = db.get("system", "bot_username")
            
            if not bot_username:
                return await message.edit("нету")

            try:
                res = await client.get_inline_bot_results(bot_username, "test")
                await client.send_inline_bot_result(
                    chat_id=message.chat.id,
                    query_id=res.query_id,
                    result_id=res.results[0].id
                )
                await message.delete()
            except Exception as e:
                await message.edit(f"Ошибка: {e}")

    @staticmethod
    async def get_inline_results(query_text):
        results = []
        if query_text == "test":
            results.append(
                types.InlineQueryResultArticle(
                    id=str(random.getrandbits(32)),
                    title="Maten Inline Test",
                    input_message_content=types.InputTextMessageContent(
                        message_text="Инлайн!"
                    )
                )
            )
        return results