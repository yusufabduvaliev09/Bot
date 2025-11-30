from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import asyncio

BOT_TOKEN = "ВАШ_ТОКЕН"
ADMIN_ID = 123456789  # замените на ваш Telegram ID
user_counter = 0

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
rt = Router()
dp.include_router(rt)


class Form(StatesGroup):
    fio = State()
    phone = State()
    pvz = State()


@rt.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await message.answer("Здравствуйте! Введите ваше ФИО:")
    await state.set_state(Form.fio)


@rt.message(Form.fio)
async def get_fio(message: types.Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await message.answer("Введите номер телефона:")
    await state.set_state(Form.phone)


@rt.message(Form.phone)
async def get_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Нариман")],
            [KeyboardButton(text="Жийдалик УПТК")],
            [KeyboardButton(text="Достук")],
        ],
        resize_keyboard=True,
    )

    await message.answer("Выберите ПВЗ:", reply_markup=kb)
    await state.set_state(Form.pvz)


@rt.message(Form.pvz)
async def get_pvz(message: types.Message, state: FSMContext):
    global user_counter
    user_counter += 1
    code = user_counter

    data = await state.get_data()
    fio = data.get("fio", "Не указано")
    phone = data.get("phone", "Не указано")
    pvz = message.text

    await state.clear()

    # Сообщение пользователю
    await message.answer(
        f"Ваш код: {code}\n"
        f"ФИО: {fio}\n"
        f"Номер: {phone}\n"
        f"ПВЗ: {pvz}\n\n"
        f"Адрес в Китае: (вставьте ваш адрес)"
    )

    # Сообщение админу
    await bot.send_message(
        ADMIN_ID,
        f"Новый пользователь!\n"
        f"Код: {code}\n"
        f"ФИО: {fio}\n"
        f"Номер: {phone}\n"
        f"ПВЗ: {pvz}"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
