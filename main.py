import sys
import uvloop, time
from colorama import Fore, Style, init
from git import Repo
from pyrogram import Client
from aiogram import Bot, Dispatcher
from utils import check_for_updates_aiogram # мне лень чо то там в init.py
#TODO: Улучшить сам загрузчик. Добавить Интеграцию Инлайн Бота, улучшить модули.
import utils
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
bot_token = config[3].split(" = ")[1]
app = Client("maten", api_id=api_id, api_hash=api_hash)

bot = Bot(token=bot_token)
dp = Dispatcher()

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

@app.on_message()
async def on_first_message(client, message):
    global started
    if not started:
        started = True
        print(app)
        asyncio.create_task(dp.start_polling(bot))      
        me = await client.get_me()
        my_id = me.id
        await bot.send_message(my_id, "[+] **Maten** запущен")
        print("[*] Aiogram запущен")
        await utils.create_group(app)
        await check_for_updates_aiogram(bot, me.id, dp)  

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