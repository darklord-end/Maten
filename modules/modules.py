# модули
from pyrogram import Client, filters
import os
import sys
import logging

logger = logging.getLogger(__name__)

class Modules:
    @staticmethod
    def register_handlers(app, prefix):
        @app.on_message(filters.command("modules", prefixes=prefix) & filters.me)
        async def modules_handler(client, message):
            main = sys.modules.get("__main__")
            LoaderMod = getattr(main, "LoaderMod", None)
            modules = list(LoaderMod.modules.keys())
            print(f"Modules: {modules}")
            if len(modules) == 0:
                await message.edit("📂 **Модули:**\n— *Список пуст*")
                return

            formatted_list = ""
            for index, m in enumerate(modules):
                char = "├──" if index < len(modules) - 1 else "└──"
                formatted_list += f"\n>{char}> >{m}>"

            caption = (
                f"**✨ Список модулей:**\n"
                f"{formatted_list}>>"
                f"\n"
                f"**Всего:** `{len(modules)}`"
            )

            await message.edit(caption)