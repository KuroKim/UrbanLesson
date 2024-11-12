# Aiogram 3.23
# Изменения в Telegram-бот:
# Кнопки главного меню дополните кнопкой "Регистрация".
# Напишите новый класс состояний RegistrationState с следующими объектами класса State: username, email, age, balance(по умолчанию 1000).
# Создайте цепочку изменений состояний RegistrationState.
# Фукнции цепочки состояний RegistrationState:
# sing_up(message):
# Оберните её в message_handler, который реагирует на текстовое сообщение 'Регистрация'.
# Эта функция должна выводить в Telegram-бот сообщение "Введите имя пользователя (только латинский алфавит):".
# После ожидать ввода имени в атрибут RegistrationState.username при помощи метода set.
# set_username(message, state):
# Оберните её в message_handler, который реагирует на состояние RegistrationState.username.
# Если пользователя message.text ещё нет в таблице, то должны обновляться данные в состоянии username на message.text. Далее выводится сообщение "Введите свой email:" и принимается новое состояние RegistrationState.email.
# Если пользователь с таким message.text есть в таблице, то выводить "Пользователь существует, введите другое имя" и запрашивать новое состояние для RegistrationState.username.
# set_email(message, state):
# Оберните её в message_handler, который реагирует на состояние RegistrationState.email.
# Эта функция должна обновляться данные в состоянии RegistrationState.email на message.text.
# Далее выводить сообщение "Введите свой возраст:":
# После ожидать ввода возраста в атрибут RegistrationState.age.
# set_age(message, state):
# Оберните её в message_handler, который реагирует на состояние RegistrationState.age.
# Эта функция должна обновляться данные в состоянии RegistrationState.age на message.text.
# Далее брать все данные (username, email и age) из состояния и записывать в таблицу Users при помощи ранее написанной crud-функции add_user.
# В конце завершать приём состояний при помощи метода finish().

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile,
                           Message)

from Bot_Token import BOT_TOKEN

from crud_functions import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

img_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = F.Field(default=1000)


kbm = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Рассчитать"), KeyboardButton(text="Информация"), KeyboardButton(text="Купить"),
         KeyboardButton(text="Регистрация")]
    ],
    resize_keyboard=True
)

kbi = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')],
    [InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
])

kbi_g = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Мужчина', callback_data='male')],
    [InlineKeyboardButton(text='Женщина', callback_data='female')]
])

kbi_b = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Товар 1', callback_data='product_buying')],
    [InlineKeyboardButton(text='Товар 2', callback_data='product_buying')],
    [InlineKeyboardButton(text='Товар 3', callback_data='product_buying')],
    [InlineKeyboardButton(text='Товар 4', callback_data='product_buying')]
])


@dp.message(F.text == "Регистрация")
async def sign_up(message: types.Message, state: FSMContext):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await state.set_state(RegistrationState.username)


@dp.message(RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    username = message.text
    if is_included(username):  # Checks if user exists in the database
        await message.answer("Пользователь существует, введите другое имя:")
    else:
        await state.update_data(username=username)
        await message.answer("Введите свой email:")
        await state.set_state(RegistrationState.email)


@dp.message(RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await message.answer("Введите свой возраст:")
    await state.set_state(RegistrationState.age)


@dp.message(RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        data = await state.get_data()
        username = data['username']
        email = data['email']

        add_user(username=username, email=email, age=age)

        await message.answer("Регистрация завершена!")
        await bot.send_photo(message.chat.id, photo=FSInputFile(os.path.join(img_dir, 'success.png')))
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите числовое значение для возраста.")


@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer(
        'Привет! Это бот. Я умею считать калории.\n'
        'Напиши /help для получения списка доступных команд.',
        reply_markup=kbm
    )


@dp.message(Command('help'))
async def help_command(message: types.Message):
    await message.answer(
        'Доступные команды:\n'
        '/start - начать работу с ботом\n'
        '/help - получить справку о доступных командах'
    )


@dp.message(F.text == 'Рассчитать')
async def main_menu(message: types.Message):
    await message.answer("Выберите опцию:", reply_markup=kbi)


@dp.callback_query(F.data == 'calories')
async def select_gender(call: types.CallbackQuery):
    await call.message.answer('Выберите ваш пол:', reply_markup=kbi_g)


@dp.callback_query(F.data.in_({'male', 'female'}))
async def set_age(call: types.CallbackQuery, state: FSMContext):
    gender = 'Мужчина' if call.data == 'male' else 'Женщина'
    await state.update_data(gender=call.data)
    await call.message.answer(f'Вы выбрали: {gender}')
    await call.message.answer('Введите свой возраст:')
    await state.set_state(UserState.age)


@dp.message(UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост:')
    await state.set_state(UserState.growth)


@dp.message(UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес:')
    await state.set_state(UserState.weight)


@dp.message(UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()

    if data['gender'] == 'male':
        bmr = 88.362 + (13.397 * data['weight']) + (4.799 * data['growth']) - (5.677 * data['age'])
    else:
        bmr = 447.593 + (9.247 * data['weight']) + (3.098 * data['growth']) - (4.330 * data['age'])

    await message.answer(f'Ваша норма калорий: {bmr:.0f} калорий.')
    await message.answer('Вернуться в начало: /start')
    await state.clear()


@dp.message(F.text == 'Информация')
async def info_command(message: types.Message):
    await message.answer(
        'Этот бот помогает рассчитать вашу норму калорий на день.\n'
        'Нажмите "Рассчитать", чтобы начать.'
    )


@dp.callback_query(F.data == 'formulas')
async def get_formulas(call: types.CallbackQuery):
    await call.message.answer(
        "Формула Миффлина-Сан Жеора:\n\n"
        "Для мужчин: BMR = 88.362 + (13.397 * вес) + (4.799 * рост) - (5.677 * возраст)\n"
        "Для женщин: BMR = 447.593 + (9.247 * вес) + (3.098 * рост) - (4.330 * возраст)"
    )


@dp.message(F.text == "Купить")
async def get_buying_list(message: types.Message):
    products = get_all_products()
    if not products:
        await message.answer("В данный момент нет в наличии.")
        return

    for product in products:
        product_id, title, description, price = product
        description_text = f"Название: {title} | Описание: {description} | Цена: {price} руб."
        img_file_path = os.path.join(img_dir, f"pr{product_id}.jpg")

        if os.path.exists(img_file_path):
            img_file = FSInputFile(path=img_file_path)
            await message.answer_photo(photo=img_file, caption=description_text)
        else:
            await message.answer(description_text)

    await message.answer("Выберите товар для покупки:", reply_markup=kbi_b)


@dp.callback_query(F.data == 'product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели товар!")
    await call.answer()


@dp.message()
async def all_messages(message: types.Message):
    await message.answer('Неизвестная команда. Напишите /help, чтобы узнать доступные команды.')


# Основная функция запуска бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
