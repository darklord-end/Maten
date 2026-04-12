import os
import sys
from git import Repo
from aiogram import types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from colorama import Fore

def get_update_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔄 Обновить", callback_data="start_update", style='success'),
            InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_update", style='danger')
        ]
    ])

async def check_for_updates_aiogram(bot, chat_id, dp):
    try:
        repo = Repo('.')
        origin = repo.remotes.origin
        origin.fetch()
        
        local_hash = repo.head.commit.hexsha
        remote_hash = origin.refs.main.commit.hexsha
        
        if local_hash != remote_hash:
            commit_msg = origin.refs.main.commit.message
            banner_url = "https://github.com/darklord-end/Imagessss/blob/main/Update.png?raw=true"
            text = (
                "🆕 <b> Доступно обновление!</b> \n"
                f"<code>⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯</code>\n"
                f"<b>Build:</b> <code>#{remote_hash[:7]}</code>\n"
                f"<b>Описание:</b> <code>{commit_msg.strip()}</code>"
            )
            await bot.send_photo(
                chat_id,
                photo=banner_url,
                caption=text,
                reply_markup=get_update_kb(),
                parse_mode="HTML"
                )
            
            @dp.callback_query(F.data == "start_update")
            async def process_update(callback: types.CallbackQuery):
                await callback.answer("Обновляюсь...")
                await callback.message.edit_text("♻️ **Обновление...**")
                try:
                    repo.remotes.origin.pull()
                    os.execv(sys.executable, [sys.executable] + sys.argv)
                except Exception as e:
                    await callback.message.answer(f"❌ Ошибка: {e}")

            @dp.callback_query(F.data == "cancel_update")
            async def cancelled_update(callback: types.CallbackQuery):
                callback.message.delete()
                await callback.answer("Нечего не делаем...")

            return True
    except Exception as e:
        print(Fore.RED + f"[!] Ошибка чекера: {e}")
    return False