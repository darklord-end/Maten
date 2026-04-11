import os
import sys
from git import Repo
from aiogram import types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from colorama import Fore

def get_update_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Обновить", callback_data="start_update", style='success')]
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_update", style='danger')]
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
            text = (
                "🆕 **Доступно обновление!**\n\n"
                f"**Коммит:** `{remote_hash[:7]}`\n"
                f"**Описание:** `{commit_msg.strip()}`"
            )
            await bot.send_message(chat_id, text, reply_markup=get_update_kb())
            
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