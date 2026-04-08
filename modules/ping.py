# Пинг
import time
from pyrogram import Client, filters

class Ping:
    @staticmethod
    def register_handlers(app, prefix):
        @app.on_message(filters.command("ping", prefixes=prefix) & filters.me)
        async def ping_handler(client, message):
            print("Ping handler called")  # Отладка
            start_time = time.perf_counter()
            await message.edit("⏳ Замеряю...")
            end_time = time.perf_counter()
            ping_ms = round((end_time - start_time) * 1000)
            await message.edit(f"<b>🏓 Pong!</b>\n<code>{ping_ms}ms</code>")

ping_instance = Ping()