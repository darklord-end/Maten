import sys
import uvloop, time
from colorama import Fore, Style, init
from git import Repo
from pyrogram import Client
from aiogram import Bot, Dispatcher
#TODO: Улучшить сам загрузчик. Добавить Интеграцию Инлайн Бота, улучшить модули.
import utils
from utils import start_automation, bot, dp, db, set_owner_id
import logging
import loggering
import asyncio
import os
logger = logging.getLogger(__name__)

uvloop.install()
from aiogram.types import Message as AiogramMessage
config = open("config.ini", "r").read().split("\n")
api_id = config[1].split(" = ")[1]
api_hash = config[2].split(" = ")[1]
app = Client("maten", api_id=api_id, api_hash=api_hash)

# тест
class LoaderMod:
    modules = {}
    aliases = {}

    @classmethod
    def add_module(cls, module_class):
        name = module_class.__name__
        cls.modules[name] = module_class
        print(Fore.GREEN + f"[*] Модуль {name} добавлен.")

    # ИЗМЕНИТЬ
    @classmethod
    def add_aliases(cls, aliases_class):
        name = aliases_class.__name__
        cls.aliases[name] = aliases_class
        print(Fore.GREEN + f"[*] Aliases {name} добавлен.")

    @classmethod
    def load_modules(cls, app):
        import os
        from utils.config import config
        pref = config.prefix
        try:
            modules_list1 = os.listdir("modules")
            modules_list2 = os.listdir("loaded")
        except:
            modules_list1 = os.listdir("modules")
        for file in modules_list1:
            if file.endswith(".py") and file != "__init__.py":
                module_name = file[:-3]
                try:
                    module = __import__(f"modules.{module_name}", fromlist=[module_name])
                    cls_name = module_name.capitalize()
                    if hasattr(module, cls_name):
                        cls.add_module(getattr(module, cls_name))
                        if hasattr(getattr(module, cls_name), 'register_handlers'):
                            getattr(module, cls_name).register_handlers(app, pref)
                except Exception as e:
                    print(Fore.RED + f"[!] Ошибка загрузки модуля {module_name}: {e}")
        if modules_list2:
            for file in modules_list2:
                if file.endswith(".py") and file != "__init__.py":
                    module_name = file[:-3]
                    print(module_name)
                    try:
                        module = __import__(f"loaded.{module_name}", fromlist=[module_name])
                        print(module)
                        cls_name = module_name if module_name[0].isupper() else module_name.capitalize()
                        print(cls_name)
                        if hasattr(module, cls_name):
                            cls.add_module(getattr(module, cls_name))
                            print(999)
                            if hasattr(getattr(module, cls_name), 'register_handlers'):
                                getattr(module, cls_name).register_handlers(app, pref)
                    except Exception as e:
                        print(Fore.RED + f"[!] Ошибка загрузки модуля {module_name}: {e}")

class Basic:
    "TODO"

init(autoreset=True)

LoaderMod.load_modules(app)

started = False
is_automating = False

@app.on_message()
async def on_first_message(client, message):
    global started, is_automating
    
    if started or is_automating:
        return
        
    if not db.get("system", "bot_token"):
        is_automating = True
        print(Fore.YELLOW + "[!] Токен не найден.")
        try:
            await utils.start_automation(client)
        finally:
            is_automating = False
            os.execl(sys.executable, sys.executable, *sys.argv) # Что-бы юб видел токен

    if not started and db.get("system", "bot_token"):
        from utils import bot, dp
        if bot and dp:
            started = True
            await utils.users.set_owner_id(client)
            asyncio.create_task(dp.start_polling(bot))
            print(Fore.GREEN + "[+] Aiogram запущен!")
            me = await client.get_me()
            await bot.send_message(me.id, "**Maten**")

def restart():
    print(Fore.YELLOW + "[*] Перезапуск...")
    os.execv(sys.executable, [sys.executable] + sys.argv)

if __name__ == "__main__":
    try:
        print(Fore.GREEN + f"[+] Maten запущен.")
        loggering.load(app)
        logger.setLevel(logging.INFO)
        logger.addHandler(loggering.loggerhandler())
        try:
            open("maten.session", "r").close()
        except FileNotFoundError:
            import setup
            print("[!] Сессия не найдена, запускаю мастер настройки...")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(setup.setup(app))
            except KeyboardInterrupt:
                os.remove("maten.session")
                sys.exit(0)
        app.run()
    except Exception as e:
        print(Fore.RED + f"[!] Maten не запущен. Ошибка: {e}")