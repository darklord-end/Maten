import uvloop, time
from colorama import Fore, Style, init
from pyrogram import Client
#TODO: Улучшить сам загрузчик. Добавить Интеграцию Инлайн Бота, улучшить модули.

uvloop.install()

app = Client("my_account", plugins=dict(root="modules"))

# тест
class LoaderMod:
    modules = {}
    aliases = {}

    @classmethod
    def add_module(cls, name, func):
        cls.modules[name] = func
        print(Fore.GREEN + f"[*] Модуль {name} добавлен.")

class Database:
    "TODO"

class Basic:
    "TODO"

init(autoreset=True)

if __name__ == "__main__":
    try:
        print(Fore.GREEN + f"[+] Maten запущен.")
        app.run()
    except Exception as e:
        print(Fore.RED + f"[!] Maten не запущен. Ошибка: {e}")