from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from games.verb_game import VerbGame
from states import AppState, VerbStates
from utils.ui import show_game_menu
from utils.diff_answer import diff_answers

verbs_router = Router()
game = VerbGame()

MODES = {
    'conjugation': 'Склонять'
}

# 1. Пользователь выбрал "Числа"
@verbs_router.message(StateFilter(AppState.verbs_game), F.text.casefold() == "глаголы")
async def choose_mode(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=MODES['conjugation']),
        KeyboardButton(text="Завершить игру")
    )
    await message.answer("Выбери режим игры:", reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(VerbStates.choosing_mode)

@verbs_router.message(StateFilter(VerbStates.choosing_mode))
async def start_end_game_or_stop(message: Message, state: FSMContext):
    if message.text == "Завершить игру":
        await show_game_menu(message, state)
        return
    if message.text == MODES['conjugation']:
        await message.answer(
            "Отлично! Начинаем игру.",
            reply_markup=ReplyKeyboardRemove()
        )
        builder = ReplyKeyboardBuilder()
        builder.row(KeyboardButton(text="Завершить игру"))
        question = game.new_end_question()

        await message.answer(f"Поставь глагол в правильную форму: {question['pronoun'].capitalize()} ({question['verb']['fi']})", reply_markup=builder.as_markup(resize_keyboard=True))
        await state.set_state(VerbStates.game_in_progress)

@verbs_router.message(StateFilter(VerbStates.game_in_progress))
async def check_end_answer(message: Message, state: FSMContext):
    if message.text == "Завершить игру":
        await show_game_menu(message, state)
        return

    data = await state.get_data()
    max_number = data.get("max_number", 100)
    answer = message.text.strip()
    correct_answer = game.get_correct_answer()

    if game.check_answer(answer):
        question = game.new_end_question()
        builder = ReplyKeyboardBuilder()
        builder.row(KeyboardButton(text="Завершить игру"))
        await message.answer(f"✅ Верно!\n\nПоставь следующий глагол в правильную форму: {question['pronoun'].capitalize()} ({question['verb']['fi']})", reply_markup=builder.as_markup(resize_keyboard=True))
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
        question = game.new_end_question()
        await message.answer(f"Поставь глагол в правильную форму: {question['pronoun'].capitalize()} ({question['verb']['fi']})", reply_markup=builder.as_markup(resize_keyboard=True))
