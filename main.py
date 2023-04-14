from typing import Union
from aiogram import Dispatcher, Bot, executor
from db_api import *
from keyboards import *


token = '5672092929:AAFlka6PX0kZvWc9pbDQ8J1rrZ1UdMR53yo'
ADMIN_ID = 889231635
PASSWORD = 'HackRachit555'
flag = False
bot = Bot(token=token)
dp = Dispatcher(bot)
db = DB()
MAIN_CFG = {
    'text': 'Bot will give you sum that you should bet and coefficient of Auto Cash Out. You should strictly follow '
            'coeffs and sums given by the bot. If you deviate from the bot strategy, you may lose.\n'
            '<b>Click Help before start.</b>',
            'parse_mode': 'HTML',
            'reply_markup': get_main_keyboard()
}


class States(enum.Enum):
    NON_STATE = 0
    ENTER_PASSWORD = 1
    ENTER_USER_ID = 2
    ENTER_TEXT_TO_SEND = 3
    

@dp.message_handler(lambda message: message.chat.id == ADMIN_ID and message.text == '/send')
async def wait_message(message: Message):
    global flag
    flag = True
    db.set_state(ADMIN_ID, States.ENTER_TEXT_TO_SEND.value)
    await message.answer('Enter text')

@dp.message_handler(
    lambda message: flag and message.chat.id == ADMIN_ID, content_types=['any']
)
async def sender(message: Message):
    global flag
    flag = False
    kwargs = {}
    if message.photo:
        f = bot.send_photo
        kwargs['photo'] = message.photo[0].file_id
        kwargs['caption'] = message.caption
    elif message.video:
        f = bot.send_video
        kwargs['video'] = message.video.file_id
    elif message.document:
        f = bot.send_document
        kwargs['document'] = message.document.file_id
        kwargs['caption'] = message.caption
    else:
        f = bot.send_message
        kwargs['text'] = message.text
    await message.answer('Рассылка началась')
    db.set_state(message.chat.id, States.NON_STATE.value)
    for user in db.get_users():
        try:
            await f(user[0], **kwargs)
        except Exception as e:
            print(str(e))

@dp.message_handler(commands=['start'])
async def start(message: Message):
    db.add_user(message.chat.id)
    await message.answer(
        'This bot helps you earn money in Aviator safe and simple. Use it wisely.\n'
        'https://telegra.ph/STRATEGY-FOR-LUCKY-JET-02-14',
        reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Ok', callback_data='enter_password'))
    )


@dp.callback_query_handler(lambda callback: callback.data == 'enter_password')
async def enter_password(callback: CallbackQuery):
    db.set_state(callback.message.chat.id, States.ENTER_PASSWORD.value)
    await bot.send_message(
        callback.message.chat.id,
        'Enter Password'
    )


@dp.callback_query_handler(lambda callback: callback.data == 'help')
async def help_answer(callback: CallbackQuery):
    await bot.send_message(
        callback.message.chat.id,
        "Minimum balance to play with bot is 500.\n\n"
        "<b>Process of using bot:</b> \n"
        "<i>"
        "Bot gives you bet amount and coefficient you should use in next round. Just follow the amounts and coeffs. "
        "Don't be afraid if you lose in round, just click lose and continue following. You will always win in the end."
        "</i>\n\n"
        "You should use Auto Cash Out.\n"
        "Only one bet button play.\n"
        "You can skip rounds\n"
        "<b>"
        "⚠️Play only with Auto Cash Out coefficient bot gave you!  Do NOT CHANGE Auto Cash Out coefficient! ⚠️"
        "</b>\n\n"
        "Good luck😉",
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton('Ok', callback_data='Ok')
            )
    )


@dp.callback_query_handler(lambda callback: callback.data in ('Ok', 'stop'))
async def ok_button(callback: CallbackQuery):
    await bot.send_message(
        callback.message.chat.id,
        **MAIN_CFG
    )


@dp.message_handler(lambda message: db.get_user(message.chat.id)[1] == States.ENTER_PASSWORD.value)
async def check_password(message: Message):
    if message.text == PASSWORD:
        db.set_state(message.chat.id, States.NON_STATE.value)
        await message.answer(
            **MAIN_CFG
        )
    else:
        await message.answer('Wrong password')
        await message.answer('Enter password')


@dp.callback_query_handler(lambda callback: callback.data == 'start_work')
async def work(callback: CallbackQuery):
    db.set_bet(callback.message.chat.id, StatusOfBet.WIN.value)
    await bot.send_message(
        callback.message.chat.id,
        f'Bet ₹{db.get_user(callback.message.chat.id)[3]} (coef {round(random.randint(15, 22)/10, 1)})',
        reply_markup=get_work_keyboard()
    )


@dp.callback_query_handler(lambda callback: callback.data == 'win')
async def work(callback: CallbackQuery):
    db.set_bet(callback.message.chat.id, StatusOfBet.WIN.value)
    await bot.send_message(
        callback.message.chat.id,
        f'Bet ₹{db.get_user(callback.message.chat.id)[3]} (coef {round(random.randint(15, 22) / 10, 1)})',
        reply_markup=get_work_keyboard()
    )


@dp.callback_query_handler(lambda callback: callback.data == 'lose')
async def work(callback: CallbackQuery):
    db.set_bet(callback.message.chat.id, StatusOfBet.LOSS.value)
    await bot.send_message(
        callback.message.chat.id,
        f'Bet ₹{db.get_user(callback.message.chat.id)[3]} (coef {round(random.randint(15, 22) / 10, 1)})',
        reply_markup=get_work_keyboard()
    )


if __name__ == '__main__':
    executor.start_polling(dp)
