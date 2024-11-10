# Создайте и дополните клавиатуры:
# В главную (обычную) клавиатуру меню добавьте кнопку "Купить".
# Создайте Inline меню из 4 кнопок с надписями "Product1", "Product2", "Product3", "Product4". У всех кнопок назначьте callback_data="product_buying"
# Создайте хэндлеры и функции к ним:
# Message хэндлер, который реагирует на текст "Купить" и оборачивает функцию get_buying_list(message).
# Функция get_buying_list должна выводить надписи 'Название: Product<number> | Описание: описание <number> | Цена: <number * 100>' 4 раза. После каждой надписи выводите картинки к продуктам. В конце выведите ранее созданное Inline меню с надписью "Выберите продукт для покупки:".
# Callback хэндлер, который реагирует на текст "product_buying" и оборачивает функцию send_confirm_message(call).
# Функция send_confirm_message, присылает сообщение "Вы успешно приобрели продукт!"

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile

from Bot_Token import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

img_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


kbm = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Рассчитать"), KeyboardButton(text="Информация"), KeyboardButton(text="Купить")]
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
    for i in range(1, 5):
        description = f"Название: Товар {i} | Описание: Пикча {i} | Цена: {i * 100} руб."
        img_file = FSInputFile(path=os.path.join(img_dir, f"pr{i}.jpg"))

        await message.answer(description)
        await message.answer_photo(photo=img_file)

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
