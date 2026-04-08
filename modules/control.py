from pyrogram import Client, filters
import os, sys, time
from utils.config import config

class Control:
    @staticmethod
    def register_handlers(app, prefix):
        
        @app.on_message(filters.command("restart", prefixes=prefix) & filters.me)
        async def restart_handler(client, message):
            await message.edit("**🔄 Перезагрузка Maten...**")
            time.sleep(1)
            os.execl(sys.executable, sys.executable, *sys.argv)  

        @app.on_message(filters.command("shutdown", prefixes=prefix) & filters.me)
        async def shutdown_handler(client, message):
            await message.edit("**🛑 Завершение работы...**")
            time.sleep(1)
            sys.exit()

        # Префикс меняется только при перезагрузке
        @app.on_message(filters.command("setprefix", prefixes=prefix) & filters.me)
        async def setprefix_handler(client, message):
            if len(message.command) < 2:
                await message.edit(f"**❌ Укажите новый префикс!**")
                return
            
            new_pref = message.command[1]
            config.set_prefix(new_pref)
            
            await message.edit(
                f"**✅ Префикс изменен на:** `{new_pref}`\n" 
            )