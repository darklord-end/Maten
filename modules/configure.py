from pyrogram import Client, filters
from aiogram import types
import random
import sys

class Configure:

    @staticmethod
    def register_handlers(app, prefix):
        @app.on_message(filters.command("setprefix", prefixes=prefix) & filters.me)
        async def setprefix_handler(client, message):
            if len(message.command) < 2:
                return await message.edit("**❌ Укажите новый префикс!**")
            
            new_pref = message.command[1]
            from utils import db
            db.set("system", "prefix", new_pref)
            
            await message.edit(f"**✅ Префикс изменен на:** `{new_pref}`\n**перезапуск...**")
            os.execv(sys.executable, [sys.executable] + sys.argv)

        @app.on_message(filters.command("config", prefixes=prefix) & filters.me)
        async def config_cmd(client, message):
            from utils import db
            bot_username = db.get("system", "bot_username")
            
            if not bot_username:
                return await message.edit("❌ **bot_username не настроен!**")

            try:
                res = await client.get_inline_bot_results(bot_username, "settings")
                await client.send_inline_bot_result(
                    chat_id=message.chat.id,
                    query_id=res.query_id,
                    result_id=res.results[0].id
                )
                await message.delete()
            except Exception as e:
                await message.edit(f"❌ **Ошибка:** `{e}`")

    @staticmethod
    async def get_inline_results(query_text):
        from utils import db
        results = []
        query = query_text.strip().lower()

        if not query or query == "settings":
            curr_pref = db.get("system", "prefix") or "."
            
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(
                    text="⚙️ Изменить префикс", 
                    switch_inline_query_current_chat=""
                )],
                [types.InlineKeyboardButton(text="❌ Закрыть", callback_data="conf_close")]
            ])

            results.append(
                types.InlineQueryResultArticle(
                    id="maten_config_main",
                    title="⚙️ Настройки Maten",
                    description=f"Текущий префикс: {curr_pref}",
                    input_message_content=types.InputTextMessageContent(
                        message_text=f"⚙️ **Панель управления Maten**\n\n• Префикс: `{curr_pref}`"
                    ),
                    reply_markup=keyboard
                )
            )

        elif len(query) == 1:
            new_pref = query
            results.append(
                types.InlineQueryResultArticle(
                    id="set_pref_action",
                    title=f"Установить префикс: {new_pref}",
                    description=f"Нажми, чтобы отправить команду .setprefix {new_pref}",
                    input_message_content=types.InputTextMessageContent(
                        message_text=f"{db.get('system', 'prefix') or '.'}setprefix {new_pref}"
                    )
                )
            )

        return results