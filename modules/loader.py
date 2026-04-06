# ИИ-СЛОП
import os, re, sys, importlib, subprocess
from pyrogram import Client, filters

MOD_DIR = "modules"
DANGER = [".session", "telethon", "pyrogram.Client", "rm -rf", "token",     "set_privacy",       # смена настроек приватности
    "update_profile",    # смена имени/био без спроса
    "phone_number",      # доступ к номеру телефона
    "export_session",    # попытка выгрузить сессию
    "account.delete"]

# Функция для быстрой установки библиотек (тихий режим)
def pip_install(libs):
    for lib in libs:
        subprocess.run([sys.executable, "-m", "pip", "install", lib.strip(), "--quiet"])

@Client.on_message(filters.command("pkg", prefixes=".") & filters.me)
async def pkg_checker(client, message):
    if not message.reply_to_message or not message.reply_to_message.document:
        return await message.edit("❌ Ответь на файл .py")
    
    # 1. Сканирование
    doc = message.reply_to_message.document
    tmp_path = await client.download_media(message.reply_to_message)
    with open(tmp_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 2. Поиск угроз и зависимостей
    urls = list(set(re.findall(r'https?://[^\s<>"]+', content)))
    danger_found = [w for w in DANGER if w in content.lower()]
    req_match = re.search(r"#\s*requires:\s*([\w\s,.-]+)", content)
    libs = [l.strip() for l in req_match.group(1).split(",")] if req_match else []

    # 3. Сохранение в память
    client.pending_pkg = {"name": doc.file_name, "path": tmp_path, "libs": libs}

    # 4. Простой текстовый отчет
    res = [f"📦 <b>Модуль:</b> <code>{doc.file_name}</code>"]
    if danger_found: res.append(f"❌ <b>ОПАСНО:</b> <code>{', '.join(danger_found)}</code>")
    if libs: res.append(f"⚙️ <b>Нужны либы:</b> <code>{', '.join(libs)}</code>")
    if urls: res.append(f"🔗 <b>Ссылки:</b>\n" + "\n".join(f"▫️ {u}" for u in urls[:3]))
    
    res.append("\n<b>Установить?</b> <code>.y</code> | <code>.n</code>")
    await message.edit("\n".join(res))

@Client.on_message(filters.command("y", prefixes=".") & filters.me)
async def confirm_pkg(client, message):
    data = getattr(client, "pending_pkg", None)
    if not data: return await message.edit("❌ Нечего подтверждать")

    await message.edit(f"⏳ Установка <code>{data['name']}</code>...")
    try:
        # Установка либ
        if data["libs"]: pip_install(data["libs"])

        # Перенос и запуск
        final_path = os.path.join(MOD_DIR, data["name"])
        os.rename(data["path"], final_path)
        
        mod_name = data["name"].replace(".py", "")
        imp_path = f"{MOD_DIR}.{mod_name}"
        
        # Импорт
        mod = importlib.reload(sys.modules[imp_path]) if imp_path in sys.modules else importlib.import_module(imp_path)

        # Регистрация команд
        for n in dir(mod):
            obj = getattr(mod, n)
            if hasattr(obj, "handlers"):
                for handler, group in obj.handlers: client.add_handler(handler, group)

        await message.edit(f"✅ <b>{mod_name}</b> готов к работе!")
    except Exception as e:
        await message.edit(f"❌ <b>Ошибка:</b>\n<code>{e}</code>")
    finally:
        client.pending_pkg = None

@Client.on_message(filters.command("n", prefixes=".") & filters.me)
async def cancel_pkg(client, message):
    data = getattr(client, "pending_pkg", None)
    if data and os.path.exists(data["path"]): os.remove(data["path"])
    client.pending_pkg = None
    await message.edit("❌ Отменено.")
