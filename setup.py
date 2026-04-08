#TODO Автоматическая установка Maten
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded
from main import restart
import os
from getpass import getpass

async def setup(client: Client):
    await client.connect()
    print("Hello! Welcome to Maten userbot setup. Please select your language: [EN/ru]")
    lang = input("Language: ").strip().lower() == 'ru'
    if lang:
        phone_number = input("Введи номер телефона: ")
        if not phone_number:
            os.remove("maten.session")
            return
        sent_code = await client.send_code(phone_number)
        code = input("Введи код, который пришел тебе в Telegram: ")
        if not code:
            os.remove("maten.session")
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
            os.remove("maten.session")
            return
        sent_code = await client.send_code(phone_number)
        code = input("Enter the code you received in Telegram: ")
        if not code:
            os.remove("maten.session")
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
    os.remove("maten.session")