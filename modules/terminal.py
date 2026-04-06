from pyrogram import Client, filters
import subprocess

@Client.on_message(filters.command("term", prefixes=".") & filters.me)
async def xz_kak_nazbati(client, message):
    cmd = message.text.split(None, 1)[1]
    result = subprocess.getoutput(cmd)
    await message.edit("Команда: " + cmd + "\nРезультат: " + result + "\n")
