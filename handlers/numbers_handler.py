# handlers/numbers_handler.py
from aiogram import Router, F
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import ReplyKeyboardRemove

from games import NumbersGame
from states import AppState

numbers_router = Router()
game = NumbersGame()

# 1. Пользователь выбрал "Числа"
@numbers_router.message(StateFilter(AppState.choosing_game_type), F.text.casefold() == "числа")
async def choose_difficulty(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Лёгкий"),
        KeyboardButton(text="Средний"),
        KeyboardButton(text="Сложный")
    )
    await message.answer("Выбери уровень сложности:", reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(AppState.choosing_game_subtype)

# 2. Пользователь выбрал уровень сложности
@numbers_router.message(StateFilter(AppState.choosing_game_subtype))
async def start_game(message: Message, state: FSMContext):
    difficulty = message.text.lower()
    if difficulty == "лёгкий":
        max_number = 10
    elif difficulty == "средний":
        max_number = 100
    elif difficulty == "сложный":
        max_number = 1000
    else:
        await message.answer("Пожалуйста, выбери уровень из предложенных.")
        return
    await message.answer(
        "Отлично! Начинаем игру.",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.update_data(max_number=max_number)
    number = game.new_question(max_number)
    await message.answer(f"Напиши число словами: {number}")
    await state.set_state(AppState.game_in_progress)

# 3. Игра в процессе
@numbers_router.message(StateFilter(AppState.game_in_progress))
async def check_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    max_number = data.get("max_number", 100)
    answer = message.text.strip()
    correct_answer = game.get_correct_answer()

    if game.check_answer(answer):
        number = game.new_question(max_number)
        await message.answer(f"✅ Верно!\n\nСледующее число: {number}")
    else:
        highlighted = game.diff_answers(answer, correct_answer)
        await message.answer(
            f"❌ Неверно.\nТвой ответ с ошибками выделенными *звёздочками*:\n<code>{highlighted}</code>\nПравильный ответ:\n<code>{correct_answer}</code>\nПопробуй следующий.",
            parse_mode="HTML"
        )
        number = game.new_question(max_number)
        await message.answer(f"Напиши число словами: {number}")
