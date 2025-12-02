import traceback

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from db.db import get_or_create_user
from handlers.verbs_handler import choose_mode as verbs_start
from handlers.weather_handler import choose_mode as weather_start
from states import AppState
from handlers.numbers_handler import choose_difficulty as numbers_choose_difficulty
from handlers.colors_handler import choose_mode as colors_start
from handlers.nouns_handler import choose_mode as nouns_start
from handlers.clock_handler import start_game as clock_start
from utils.ui import show_game_menu

start_router = Router()

@start_router.message(StateFilter(None))
async def cmd_start(message: Message, state: FSMContext):
    user = await get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name or message.from_user.first_name,
    )
    print(f"User from DB: {user}")
    await show_game_menu(message, state)

@start_router.message(StateFilter(AppState.choosing_game_type))
async def choose_game(message: Message, state: FSMContext):
    try:
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
        elif text == "погода":
            await state.set_state(AppState.weather_game)
            await message.answer("Вы выбрали игру Погода. Начинаем!")
            await weather_start(message, state)
        elif text == "существительные":
            await state.set_state(AppState.nouns_game)
            await message.answer("Вы выбрали игру Существительные. Начинаем!")
            await nouns_start(message, state)
        elif text == "время":
            await state.set_state(AppState.clock_game)
            await message.answer("Вы выбрали игру Время. Начинаем!")
            await clock_start(message, state)
        else:
            await message.answer("Пожалуйста, выберите игру, используя кнопки.")
    except Exception as e:
        print("Ошибка:", e)
        traceback.print_exc()
        await message.answer("Пожалуйста, выберите из предложенных вариантов.")
