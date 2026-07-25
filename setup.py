from pyrogram import Client
from pyrogram.errors import (
    SessionPasswordNeeded,
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    FloodWait
)
import os
import sys
import asyncio
from getpass import getpass
from colorama import Fore, init

init(autoreset=True)

def read_config():
    api_id = None
    api_hash = None
    try:
        with open("config.ini", "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("api_id"):
                    api_id = line.split(" = ")[1]
                elif line.startswith("api_hash"):
                    api_hash = line.split(" = ")[1]
    except FileNotFoundError:
        pass
    return api_id, api_hash

async def setup():
    print(Fore.CYAN + "Hello! Welcome to Maten userbot setup.")
    lang = input("Please select your language [EN/RU]: ").strip().lower()
    is_ru = lang == 'ru'

    def input_with_prompt(prompt, validator=None, error_msg="Invalid input"):
        while True:
            value = input(prompt).strip()
            if not value:
                print(Fore.RED + "Input cannot be empty.")
                continue
            if validator and not validator(value):
                print(Fore.RED + error_msg)
                continue
            return value

    def validate_api_id(val):
        return val.isdigit()

    def validate_api_hash(val):
        return len(val) >= 32

    existing_api_id, existing_api_hash = read_config()
    api_id = None
    api_hash = None

    if existing_api_id and existing_api_hash:
        msg = "Use existing config.ini? [Y/n]: " if not is_ru else "Использовать существующий config.ini? [Y/n]: "
        use_existing = input(msg).strip().lower()
        if use_existing != 'n':
            api_id = existing_api_id
            api_hash = existing_api_hash

    if not api_id or not api_hash:
        print(Fore.YELLOW + ("You need to obtain API ID and API Hash from my.telegram.org" if not is_ru else
                             "Вам нужно получить API ID и API Hash на my.telegram.org"))
        api_id = input_with_prompt(
            "Enter API ID: " if not is_ru else "Введите API ID: ",
            validator=validate_api_id,
            error_msg="API ID must be a number."
        )
        api_hash = input_with_prompt(
            "Enter API HASH: " if not is_ru else "Введите API HASH: ",
            validator=validate_api_hash,
            error_msg="API HASH should be at least 32 characters."
        )

    with open("config.ini", "w") as f:
        f.write(f"[pyrogram]\napi_id = {api_id}\napi_hash = {api_hash}\n")
    print(Fore.GREEN + "[+] Config file saved.")

    if os.path.exists("maten.session"):
        msg = ("Session file found. Authorize again? [y/N]: " if not is_ru else
               "Файл сессии найден. Авторизоваться заново? [y/N]: ")
        reauth = input(msg).strip().lower()
        if reauth != 'y':
            print(Fore.GREEN + "[+] Config and session already exist. Run 'python3 main.py' manually to start.")
            sys.exit(0)
        os.remove("maten.session")

    client = Client("maten", api_id=api_id, api_hash=api_hash, ipv6=False)
    try:
        await client.connect()
        print(Fore.GREEN + "[+] Connected to Telegram servers.")
    except Exception as e:
        print(Fore.RED + f"[!] Failed to connect: {e}")
        sys.exit(1)

    phone_prompt = (
        "Enter your phone number (with country code): "
        if not is_ru else
        "Введите номер телефона (с кодом страны): "
    )
    phone_number = input_with_prompt(phone_prompt)

    try:
        sent_code = await client.send_code(phone_number)
        print(Fore.GREEN + "[+] Code sent to your Telegram.")
    except FloodWait as e:
        print(Fore.RED + f"[!] Please wait {e.x} seconds before retrying.")
        await client.disconnect()
        sys.exit(1)
    except Exception as e:
        print(Fore.RED + f"[!] Failed to send code: {e}")
        await client.disconnect()
        sys.exit(1)

    code_prompt = (
        "Enter the code you received: "
        if not is_ru else
        "Введите код, полученный в Telegram: "
    )
    code = input_with_prompt(code_prompt)

    try:
        user = await client.sign_in(
            phone_number=phone_number,
            phone_code_hash=sent_code.phone_code_hash,
            phone_code=code
        )
    except SessionPasswordNeeded:
        print(Fore.YELLOW + (
            "Two-factor authentication enabled." if not is_ru else
            "Включена двухфакторная аутентификация."
        ))
        password = getpass(
            "Enter 2FA password: " if not is_ru else "Введите пароль 2FA: "
        )
        try:
            user = await client.check_password(password)
        except Exception as e:
            print(Fore.RED + f"[!] 2FA error: {e}")
            await client.disconnect()
            sys.exit(1)
    except PhoneCodeInvalid:
        print(Fore.RED + (
            "Invalid code. Please restart setup." if not is_ru else
            "Неверный код. Перезапустите установку."
        ))
        await client.disconnect()
        sys.exit(1)
    except PhoneCodeExpired:
        print(Fore.RED + (
            "Code expired. Please restart setup." if not is_ru else
            "Код истек. Перезапустите установку."
        ))
        await client.disconnect()
        sys.exit(1)
    except Exception as e:
        print(Fore.RED + f"[!] Error during sign-in: {e}")
        await client.disconnect()
        sys.exit(1)

    print(Fore.GREEN + f"[+] Logged in as {user.first_name} (ID: {user.id})")
    await client.disconnect()
    print(Fore.GREEN + "[+] Session saved!")
    print(Fore.GREEN + "[+] Run 'python3 main.py' manually to start Maten.")

if __name__ == "__main__":
    asyncio.run(setup())