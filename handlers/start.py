from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from handlers.verbs_handler import choose_mode as verbs_start
from states import AppState
from handlers.numbers_handler import choose_difficulty as numbers_choose_difficulty
from handlers.colors_handler import choose_mode as colors_start
from utils.ui import show_game_menu

start_router = Router()

@start_router.message(StateFilter(None))
async def cmd_start(message: Message, state: FSMContext):
    await show_game_menu(message, state)

@start_router.message(StateFilter(AppState.choosing_game_type))
async def choose_game(message: Message, state: FSMContext):
    text = message.text.strip().lower()
    if text == "числа":
        await state.set_state(AppState.numbers_game)
        await message.answer("Вы выбрали игру Числа. Начинаем!")
        await numbers_choose_difficulty(message, state)
    elif text == "цвета":
        await state.set_state(AppState.colors_game)
        await message.answer("Вы выбрали игру Цвета. Начинаем!")
        await colors_start(message, state)
    elif text == "глаголы":
        await state.set_state(AppState.verbs_game)
        await message.answer("Вы выбрали игру Глаголы. Начинаем!")
        await verbs_start(message, state)
    else:
        await message.answer("Пожалуйста, выберите игру, используя кнопки.")
