# Fun module | By: @DarkLord
import random
import time
from pyrogram import Client, filters

class Random:
    @staticmethod
    def register_handlers(app, prefix):
        
        @app.on_message(filters.command("random", prefixes=prefix) & filters.me)
        async def random_handler(client, message):
            if len(message.command) < 2:
                await message.edit("**❓ Напиши событие после команды**\n*(например: .random я сегодня высплюсь)*")
                return

            question = " ".join(message.command[1:])
            choices = ["✅ Да", "❌ Нет", "🤔 Возможно", "🤫 Секрет"]
            result = random.choice(choices)

            await message.edit(f"**🧐 Гадаю на:** `{question}`\n**Результат:** `⏳ Думаю...`")
            time.sleep(1.5)

            await message.edit(
                f"**❓ Вопрос:** `{question}`\n"
                f"**✨ Ответ:** **{result}**"
            )