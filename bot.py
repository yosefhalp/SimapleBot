import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from time import sleep
from config import *

logging.basicConfig(level=logging.INFO)


bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    name = State()
    age = State()
    gender = State()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await Form.name.set()
    await message.reply("היי הגעת לבוט מבית @TermuxIL **קבוצת ההאקינג של ישראל**\nמה השם שלך", parse_mode='markdown')


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await Form.next()
    await message.reply("אוקיי, מה הגיל שלך?")


@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.age)
async def process_age_invalid(message: types.Message):
    return await message.reply("הגיל צריך להיות במספרים בלבד ❗️\n מה הגיל שלך")


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    await Form.next()
    await state.update_data(age=int(message.text))

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("גבר", "אישה")
    markup.add("אחר")

    await message.reply("מה המין שלך?", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["גבר", "אישה", "אחר"], state=Form.gender)
async def process_gender_invalid(message: types.Message):
    return await message.reply("יש לבחור מהמקלדת בלבד ❗️")


@dp.message_handler(state=Form.gender)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text
        markup = types.ReplyKeyboardRemove()
        await bot.send_message(chat_id=int(LOG_CHANNEL),
                               text=md.text(
                                   md.text('משתמש חדש! ', md.bold(data['name'])),
                                   md.text('הגיל: ', md.code(data['age'])),
                                   md.text('המין:', data['gender']),
                                   md.text('שם משתמש: ', message.from_user.first_name),
                                   md.text('id: ', message.from_user.id),
                                   sep='\n',
                               ),
                               parse_mode=ParseMode.MARKDOWN
                               )

        keyboard_markup = InlineKeyboardMarkup(row_width=3)
        keyboard_markup.add(InlineKeyboardButton(text="לערוץ שלנו 📌", url="https://t.me/joinchat""/T7_1ahI6b9O8N0Ih"),
                InlineKeyboardButton(text="לקבוצה שלנו 🖥",url="https://t.me/joinchat/VA5XFTr3g_JoT3Gs"),
                InlineKeyboardButton(text="לתמיכה באפליקציות 📱", url="https://t.me/TermuxILapk"),
                InlineKeyboardButton(text="לשיתוף הקבוצה 🎁", url="https://telegram.me/share/url?url=https://t.me/joinchat/VA5XFTr3g_JoT3Gs"),
                InlineKeyboardButton(text="לתרומות 💵", url="https://t.me/TermuxILDonate"),
                InlineKeyboardButton(text="לקוד מקור 📜", url="https://github.com/Deleted-accounts/SimapleBot"))

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

        await bot.send_message(chat_id=message.chat.id,
                               text=md.text(
                                   md.text('היי ', md.bold(data['name'])),
                                   md.text('הגיל שלך הוא: ', md.code(data['age'])),
                                   md.text('המין:', data['gender']),
                                   md.text('שם משתמש: ', message.from_user.first_name),
                                   sep='\n',
                               ),
                               reply_markup=markup,
                               parse_mode=ParseMode.MARKDOWN
                               )
        sleep(2)
        await bot.send_message(message.chat.id, text="למעבר לערוצים שלנו בחר בקישורים הבאים:"
                                                     " פקודות זמינות לבינתיים: /info", reply_markup=keyboard_markup)

    await state.finish()


@dp.message_handler(commands="info")
async def check_language(message: types.Message):
    locale = message.from_user.locale

    await message.reply(md.text(
        md.bold('מידע על השפה שלך: '),
        md.text('🔸', md.bold('קוד מדינה: '), md.code(locale.language)),
        md.text('🔸', md.bold('טריטוריה: '), md.code(locale.territory or 'לא ידוע ')),
        md.text('🔸', md.bold('שם שפה: '), md.code(locale.language_name)),
        md.text('🔸', md.bold('שם השפה באנגלית: '), md.code(locale.english_name)),
        sep='\n'
        ),
        parse_mode=ParseMode.MARKDOWN
        )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
