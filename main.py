import uvloop, time
from colorama import Fore, Style, init
from pyrogram import Client
#TODO: Улучшить сам загрузчик. Добавить Интеграцию Инлайн Бота, улучшить модули.
import utils
import logging
import loggering

logger = logging.getLogger(__name__)

uvloop.install()
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

    @classmethod
    def load_modules(cls, app):
        import os
        for file in os.listdir("modules"):
            if file.endswith(".py") and file != "__init__.py":
                module_name = file[:-3]
                try:
                    module = __import__(f"modules.{module_name}", fromlist=[module_name])
                    cls_name = module_name.capitalize()
                    if hasattr(module, cls_name):
                        cls.add_module(getattr(module, cls_name))
                        if hasattr(getattr(module, cls_name), 'register_handlers'):
                            getattr(module, cls_name).register_handlers(app)
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
        logger.info("test")
        started = True
        await client.send_message("me", "Maten запущен!")
        print(app)
        await utils.create_group(app)

if __name__ == "__main__":
    try:
        print(Fore.GREEN + f"[+] Maten запущен.")
        loggering.load(app)
        logger.setLevel(logging.INFO)
        logger.addHandler(loggering.loggerhandler())
        app.run()
    except Exception as e:
        print(Fore.RED + f"[!] Maten не запущен. Ошибка: {e}")