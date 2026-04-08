import os
import sys
import logging
import inspect
from pyrogram import *
logger = logging.getLogger(__name__)

class Loader():
    @staticmethod
    def register_handlers(app, prefix):
        @app.on_message(filters.command("lm", prefixes=prefix) & filters.me)
        async def load_module(clent, message):
            if not message.reply_to_message or not message.reply_to_message.document:
                await message.edit("Ответьте на файл модуля, для загрузки")
                return
            file = message.reply_to_message.document
            if not file.file_name.endswith(".py"):
                await message.edit("Ответьте на файл модуля, для загрузки")
                return
            os.makedirs("loaded", exist_ok=True)
            file_path = os.path.join("loaded", file.file_name)
            await message.edit("Загрузка...")
            module_name = file.file_name[:-3]
            await app.download_media(file, file_path)
            main = sys.modules.get("__main__")
            LoaderMod = getattr(main, "LoaderMod", None)
            if not LoaderMod:
                await message.edit("Ошибка: LoaderMod не найден.")
                return
            LoaderMod.load_modules(app)
            await message.edit(f"Модуль {module_name} загружен!")
        @app.on_message(filters.command("ulm", prefixes=prefix) & filters.me)
        async def unload_module(client, message):
            if len(message.command) < 2:
                await message.edit("Укажите название модуля для выгрузки")
                return
            module_name = message.command[1]
            main = sys.modules.get("__main__")
            LoaderMod = getattr(main, "LoaderMod", None)
            if module_name not in LoaderMod.modules:
                print(1)
                if module_name.capitalize() in LoaderMod.modules:
                    print(2)
                    module_name = module_name.capitalize()
                else:
                    await message.edit("Модуль не найден!")
                    return
            source_file = inspect.getfile(LoaderMod.modules[module_name])
            if "/modules/" in source_file:
                await message.edit("Нельзя выгрузить встроенный модуль!")
                return
            os.remove(source_file)
            del LoaderMod.modules[module_name]
            main.restart()
            await message.edit(f"Модуль {module_name} выгружен!")