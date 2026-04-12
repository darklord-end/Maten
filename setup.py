#TODO Автоматическая установка Maten
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded
import os
import sys
import asyncio
from getpass import getpass

def restart():
    python = sys.executable
    os.execl(python, python, "main.py")

async def setup():
    print("Hello! Welcome to Maten userbot setup. Please select your language: [EN/ru]")
    lang = input("Language: ").strip().lower() == 'ru'

    api_id = input("Введите API ID: " if lang else "Enter API ID: ")
    api_hash = input("Введите API HASH: " if lang else "Enter API HASH: ")
    
    with open("config.ini", "w") as f:
        f.write(f"[pyrogram]\napi_id = {api_id}\napi_hash = {api_hash}\n")

    client = Client("maten", api_id=api_id, api_hash=api_hash)
    await client.connect()

    if lang:
        phone_number = input("Введи номер телефона: ")
        if not phone_number:
            if os.path.exists("maten.session"): os.remove("maten.session")
            return
        sent_code = await client.send_code(phone_number)
        code = input("Введи код, который пришел тебе в Telegram: ")
        if not code:
            if os.remove("maten.session"): os.remove("maten.session")
            return
        try:
            user = await client.sign_in(
                phone_number=phone_number,
                phone_code_hash=sent_code.phone_code_hash,
                phone_code=code
            )
        except SessionPasswordNeeded:
            user = await client.check_password(getpass("Введи пароль 2FA: ", stream=None))
        
        print("[+] Сессия сохранена!")
        await client.disconnect()
        restart()

    else:
        print("Please enter your phone number: ")
        phone_number = input("Phone number: ")
        if not phone_number:
            if os.path.exists("maten.session"): os.remove("maten.session")
            return
        sent_code = await client.send_code(phone_number)
        code = input("Enter the code you received in Telegram: ")
        if not code:
            if os.path.exists("maten.session"): os.remove("maten.session")
            return
        try:
            user = await client.sign_in(
                phone_number=phone_number,
                phone_code_hash=sent_code.phone_code_hash,
                phone_code=code
            )
        except SessionPasswordNeeded:
            user = await client.check_password(getpass("Enter your 2FA password: ", stream=None))
        
        print("[+] Session saved!")
        await client.disconnect()
        restart()

if __name__ == "__main__":
    if os.path.exists("maten.session"):
        os.remove("maten.session")
    asyncio.run(setup())