from pyrogram import Client, filters

@Client.on_message(filters.command("message", prefixes=".") & filters.me)
async def message_aaa(client, message):
    await message.edit("Тест команда!")
    await client.send_message("me", "Тест команда!")
