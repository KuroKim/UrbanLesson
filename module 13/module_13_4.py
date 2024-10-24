
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from Bot_Token import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer('Привет! Это бот.\n'
                         'Напиши /help для получения списка доступных команд.')


@dp.message(Command('help'))
async def help_command(message: types.Message):
    await message.answer('Доступные команды:\n'
                         '/start - начать работу с ботом\n'
                         '/help - получить справку о доступных командах\n'
                         '/Calories - рассчитать норму калорий.')


@dp.message(Command('Calories'))
async def set_age(message: types.Message, state: FSMContext):
    await message.answer('Введите свой возраст:')
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
    bmr = 88.362 + (13.397 * data['weight']) + (4.799 * data['growth']) - (5.677 * data['age'])
    await message.answer(f'Ваша норма калорий: {bmr:.0f} калорий.')
    await state.clear()


@dp.message()
async def all_messages(message: types.Message):
    await message.answer('Неизвестная команда. Напишите /help, чтобы узнать доступные команды.')


# Основная функция запуска бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
