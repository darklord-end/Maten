# сам делал :sunglasses:
from pyrogram import Client, filters
import speedtest

class SpeedTest:
    @staticmethod
    def register_handlers(app):
        @app.on_message(filters.command("speedtest", prefixes=".") & filters.me)
        async def speedtest_handler(client, message):
            st = speedtest.Speedtest()
            await message.edit("Поиск лучшего сервера...")
            st.get_best_server()
            await message.edit("Измеряем скорость скачивания...")
            download_speed = st.download() / 1_000_000
            await message.edit("Измеряем скорость загрузки...")
            upload_speed = st.upload() / 1_000_000
            await message.edit("Тестирование скорости завершено...")
            await message.edit(f"Скорость скачивание: {download_speed:.2f} Мбит/с\
        nСкорость загрузки: {upload_speed:.2f}, \nПинг: {st.results.ping}") 
    