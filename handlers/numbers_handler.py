from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from games import NumbersGame
from states import AppState, NumbersStates
from utils.ui import show_game_menu
from utils.diff_answer import diff_answers

numbers_router = Router()


@numbers_router.message(StateFilter(AppState.numbers_game), F.text.casefold() == "числа")
async def choose_difficulty(message: Message, state: FSMContext):
    game = NumbersGame()
    await state.update_data(game=game)
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Лёгкий"),
        KeyboardButton(text="Средний"),
        KeyboardButton(text="Сложный"),
        KeyboardButton(text="Завершить игру")
    )
    await message.answer(
        "Правила: будет загадано число (от 1 до 10, 100 или 1000). Нужно написать загаданное число на финском.\nИгра идёт до 10 вопросов.\n\nВыбери уровень сложности:",
        reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(NumbersStates.choosing_difficulty)


@numbers_router.message(StateFilter(NumbersStates.choosing_difficulty))
async def start_game_or_stop(message: Message, state: FSMContext):
    data = await state.get_data()
    game: NumbersGame = data.get("game")
    if message.text == "Завершить игру":
        await state.set_state(AppState.choosing_game_type)
        await show_game_menu(message, state)
        return

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

    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Завершить игру"))

    await message.answer(f"Напиши число словами: {number}", reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(NumbersStates.game_in_progress)


@numbers_router.message(StateFilter(NumbersStates.game_in_progress))
async def check_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    game: NumbersGame = data.get("game")
    if message.text == "Завершить игру":
        await show_game_menu(message, state)
        return

    data = await state.get_data()
    max_number = data.get("max_number", 100)
    answer = message.text.strip()
    correct_answer = game.get_correct_answer()

    if game.check_answer(answer):
        number = game.new_question(max_number)
        builder = ReplyKeyboardBuilder()
        builder.row(KeyboardButton(text="Завершить игру"))
        await message.answer(f"✅ Верно!\n\nСледующее число: {number}",
                             reply_markup=builder.as_markup(resize_keyboard=True))
    else:
        highlighted = diff_answers(answer, correct_answer)
        builder = ReplyKeyboardBuilder()
        builder.row(KeyboardButton(text="Завершить игру"))
        await message.answer(
            f"❌ Неверно.\nТвой ответ с ошибками выделенными *звёздочками*:\n<code>{highlighted}</code>\n"
            f"Правильный ответ:\n<code>{correct_answer}</code>\nПопробуй следующий.",
            parse_mode="HTML",
            reply_markup=builder.as_markup(resize_keyboard=True)
        )
        if game.inner_count == 10:
            await message.answer(f"Игра заверешна! Итого правильных ответов: {game.correct_count}/{game.inner_count}")
            await show_game_menu(message, state)
            return
        else:
            number = game.new_question(max_number)
            await message.answer(f"Напиши число словами: {number}",
                                 reply_markup=builder.as_markup(resize_keyboard=True))
