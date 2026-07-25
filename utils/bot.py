import sys
import aiohttp
from db import Database
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import BufferedInputFile, InputProfilePhotoStatic

db = Database()
bot_token = db.get("system", "bot_token")
dp = Dispatcher()

if bot_token:
    bot = Bot(token=bot_token)
else:
    print("[!] Токен не найден в базе данных")
    bot = None

async def check_bot_pfp(target_bot=None):
    current_bot = target_bot or bot
    if not current_bot:
        return

    try:
        bot_me = await current_bot.get_me()
        photos = await current_bot.get_user_profile_photos(bot_me.id)
        if photos and photos.total_count > 0:
            print("[*] Аватарка уже установлена, пропускаем.")
            return

        print("[*] Авы нет, качаю в память и ставлю...")
        pfp_url = "https://raw.githubusercontent.com/darklord-end/Imagessss/refs/heads/main/Logo2.png"

        async with aiohttp.ClientSession() as sess:
            async with sess.get(pfp_url) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    input_file = BufferedInputFile(data, filename="pfp.png")
                    photo = InputProfilePhotoStatic(photo=input_file)
                    await current_bot.set_my_profile_photo(photo=photo)
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


@dp.callback_query(F.data == "logs")
async def logs_callback(callback: types.CallbackQuery):
    await callback.answer("📔 Логи пока не реализованы", show_alert=True)


@dp.callback_query(F.data == "settings")
async def settings_callback(callback: types.CallbackQuery):
    from utils.config import config
    pref = config.prefix
    await callback.message.edit_caption(
        caption=f"⚙️ **Настройки Maten**\n\n• Префикс: `{pref}`",
        parse_mode="Markdown"
    )
    await callback.answer()


@dp.callback_query(F.data == "conf_close")
async def conf_close_callback(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.answer()