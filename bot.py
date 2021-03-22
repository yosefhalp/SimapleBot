from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.utils.executor import start_polling
import logging
from .config import *

logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(msg: Message):
    try:
        await bot.send_message(
            int(LOG_CHANNEL),
            f"#NEW_USER: \n\nמשתמש חדש {msg.from_user.first_name} {msg.from_user.id} התחיל עם הבוט! ")
    except Exception:
        pass

    # termux IL links
    keyboard_markup = InlineKeyboardMarkup(row_width=3)
    keyboard_markup.add(InlineKeyboardButton(text="לערוץ שלנו 📌", url="https://t.me/joinchat"
                                                                       "/T7_1ahI6b9O8N0Ih"),
                        InlineKeyboardButton(text="לקבוצה שלנו 🖥",
                                             url="https://t.me/joinchat/VA5XFTr3g_JoT3Gs"),
                        InlineKeyboardButton(text="לתמיכה באפליקציות 📱", url="https://t.me/TermuxILapk"),
                        InlineKeyboardButton(text="לקוד מקור 📜", url="https://github.com/Deleted-accounts/SimapleBot"),
                        InlineKeyboardButton(text="לתרומות 💵", url="https://t.me/TermuxILDonate"))

    # creator credit
    if creator_link.startswith('@'):
        new_url = creator_link.replace('@', 'https://t.me/')
        keyboard_markup.add(InlineKeyboardButton(text=cretorBt, url=new_url))
    elif creator_link.startswith('https://t.me/'):
        keyboard_markup.add(InlineKeyboardButton(text=cretorBt, url=creator_link))
    else:
        pass

    # other buttons
    if bt1 and bt1url:
        keyboard_markup.add(InlineKeyboardButton(text=bt1, url=bt1url))
    elif bt1 and bt2 and bt1url and bt2url:
        keyboard_markup.add(InlineKeyboardButton(text=bt1, url=bt1url), InlineKeyboardButton(text=bt2, url=bt2url))
    else:
        pass

    await bot.send_message(msg.chat.id, text=f" היי { msg.from_user.first_name}\n\nהגעת לרובוט דוגמא מבית @TermuxIL "
                                             f"אתה מוזמן ללחוץ על "
                                             "הקישורים הבאים...", reply_markup=keyboard_markup)

if __name__ == '__main__':
    start_polling(dp)
