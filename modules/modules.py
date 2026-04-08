# модули
from pyrogram import Client, filters
import os

class Modules:
    @staticmethod
    def register_handlers(app, prefix):
        @app.on_message(filters.command("modules", prefixes=prefix) & filters.me)
        async def modules_handler(client, message):
            folder = "modules"
            
            if not os.path.exists(folder):
                await message.edit("❌ **Папка `modules/` не найдена**")
                return

            modules = [m for m in os.listdir(folder) if not m.startswith(("_", "."))]

            if not modules:
                await message.edit("📂 **Модули:**\n— *Список пуст*")
                return

            formatted_list = ""
            for i, m in enumerate(modules):
                char = "├──" if i < len(modules) - 1 else "└──"
                formatted_list += f"\n`{char}` `{m}`"

            caption = (
                f"**✨ Список модулей:**\n"
                f"{formatted_list}"
                f"\n"
                f"**Всего:** `{len(modules)}`"
            )

            await message.edit(caption)