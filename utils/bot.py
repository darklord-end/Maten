import sys
import aiohttp
from db import Database
from aiogram import Bot, Dispatcher, types
from aiogram.client.session.aiohttp import AiohttpSession
import sys

db = Database()
session = AiohttpSession()
bot_token = db.get("system", "bot_token")

if bot_token:
    bot = Bot(token=bot_token)
    dp = Dispatcher()
else:
    dp = None
    bot = None

@dp.inline_query()
async def global_inline_handler(query: types.InlineQuery):
    text = query.query.strip().lower()
    print(f"DEBUG: Пришел запрос от {query.from_user.username}: {text}")
    
    results = []
    
    if text == "ping":
        results.append(
            types.InlineQueryResultArticle(
                id="ping_test",
                title="PONG!",
                input_message_content=types.InputTextMessageContent(message_text="Бот живой!")
            )
        )

    main = sys.modules.get("__main__")
    loader = getattr(main, "LoaderMod", None)

    if loader:
        for module_cls in loader.modules.values():
            if hasattr(module_cls, "get_inline_results"):
                try:
                    mod_res = await module_cls.get_inline_results(text)
                    if mod_res:
                        results.extend(mod_res)
                except Exception as e:
                    print(f"DEBUG ERROR in {module_cls.__name__}: {e}")

    print(f"DEBUG: Отправляю {len(results)} результатов")
    await query.answer(results, cache_time=2, is_personal=True)
