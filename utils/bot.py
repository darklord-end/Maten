import sys
import aiohttp
from db import Database
from aiogram import Bot, Dispatcher, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import URLInputFile, BufferedInputFile
import io
import sys

db = Database()
session = AiohttpSession()
bot_token = db.get("system", "bot_token")
dp = Dispatcher()

if bot_token:
    bot = Bot(token=bot_token)
else:
    print("[!] Токен не найден в базе данных")
    bot = None

# Говно какоето из Bot Api 9.4 
async def check_bot_pfp(target_bot=None):
    current_bot = target_bot or bot
    if not current_bot: return
    
    try:
        me = await current_bot.get_me()
        chat = await current_bot.get_chat(me.id)
        
        print("[*] Авы нет, качаю в память и ставлю...")
        pfp_url = "https://github.com/darklord-end/Imagessss/blob/main/Info.png?raw=true"
            
        async with aiohttp.ClientSession() as sess:
            async with sess.get(pfp_url) as resp:
                if resp.status == 200:
                     # Читаем картинку в байты прямо в оперативку
                    data = await resp.read()
                    # Создаем "виртуальный" файл из байтов
                    input_file = BufferedInputFile(data, filename="pfp.png")
                        
                    await current_bot.set_my_profile_photo(photo=input_file)
                    print("[+] Аватарка успешно установлена из памяти!")
    except Exception as e:
        print(f"[!] Ошибка pfp: {e}")


@dp.inline_query()
async def global_inline_handler(query: types.InlineQuery):
    if not bot:
        return
    text = query.query.strip().lower()
    print(f"[*] Пришел запрос от {query.from_user.username}: {text}")
    
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
                    print(f"[!] ERROR in {module_cls.__name__}: {e}")

    print(f"[*] Отправляю {len(results)} результатов")
    await query.answer(results, cache_time=2, is_personal=True)
