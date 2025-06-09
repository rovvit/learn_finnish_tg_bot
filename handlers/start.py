# handlers/start.py
from aiogram import Router
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton

from states import AppState

HELP_COMMANDS = """
Список команд:
/start - начать
/help - помощь
/stop - выйти из игры
"""

start_router = Router()

@start_router.message(StateFilter(None), CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Числа"))
    await message.answer("Выбери во что играть", reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(AppState.choosing_game_type)

@start_router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(HELP_COMMANDS)

@start_router.message(Command("stop"))
async def cmd_stop(message: Message, state: FSMContext):
    await message.answer("Игра остановлена.")
    await state.set_state(AppState.choosing_game_type)