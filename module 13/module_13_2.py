import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage

from Bot_Token import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

router = dp.message


@router(CommandStart())
async def start_command(message: types.Message):
    print('Привет! Я бот помогающий твоему здоровью.' )
    await message.answer('Привет! Это бот.\n'
                         'Напиши /help для получения списка доступных команд.')


@router(Command('help'))
async def help_command(message: types.Message):
    await message.answer('Доступные команды:\n'
                         '/start - начать работу с ботом\n'
                         '/help - получить справку о доступных командах')


@router()
async def all_messages(message: types.Message):
    print('Введите команду /start, чтобы начать общение.')

    await message.answer('Неизвестная команда. Напишите /start, чтобы начать общение.')


# Основная функция запуска бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
