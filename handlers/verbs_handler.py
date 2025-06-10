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
    'conjugation': 'Склонять',
    'choose_one_fi_ru': 'Выбор перевода (FI-RU)',
    'choose_one_ru_fi': 'Выбор перевода (RU-FI)'
}

# 1. Пользователь выбрал "Числа"
@verbs_router.message(StateFilter(AppState.verbs_game), F.text.casefold() == "глаголы")
async def choose_mode(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=MODES['conjugation']),
        KeyboardButton(text=MODES['choose_one_ru_fi']),
        KeyboardButton(text=MODES['choose_one_fi_ru'])
    )
    builder.row(
        KeyboardButton(text="Завершить игру")
    )
    await message.answer("Выбери режим игры:", reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(VerbStates.choosing_mode)

@verbs_router.message(StateFilter(VerbStates.choosing_mode))
async def start_end_game_or_stop(message: Message, state: FSMContext):
    if message.text == "Завершить игру":
        await show_game_menu(message, state)
        return
    if message.text == MODES['choose_one_ru_fi']:
        await message.answer(
            "Отлично! Начинаем игру.",
            reply_markup=ReplyKeyboardRemove()
        )
        builder = ReplyKeyboardBuilder()
        builder.row(
            KeyboardButton(text="4 варианта"),
            KeyboardButton(text="8 вариантов"),
            KeyboardButton(text="12 вариантов"),
            KeyboardButton(text="Завершить игру")
        )
        await state.update_data(mode='ru-fi')
        await message.answer(
            f"Выбери количество вариантов:",
            reply_markup=builder.as_markup(resize_keyboard=True))
        await state.set_state(VerbStates.choosing_difficulty)
    if message.text == MODES['choose_one_fi_ru']:
        await message.answer(
            "Отлично! Начинаем игру.",
            reply_markup=ReplyKeyboardRemove()
        )
        builder = ReplyKeyboardBuilder()
        builder.row(
            KeyboardButton(text="4 варианта"),
            KeyboardButton(text="8 вариантов"),
            KeyboardButton(text="12 вариантов"),
            KeyboardButton(text="Завершить игру")
        )
        await state.update_data(mode='fi-ru')
        await message.answer(
            f"Выбери количество вариантов:",
            reply_markup=builder.as_markup(resize_keyboard=True))
        await state.set_state(VerbStates.choosing_difficulty)
    if message.text == MODES['conjugation']:
        await message.answer(
            "Отлично! Начинаем игру.",
            reply_markup=ReplyKeyboardRemove()
        )
        builder = ReplyKeyboardBuilder()
        builder.row(KeyboardButton(text="Завершить игру"))
        question = game.new_word_question()

        await message.answer(f"Поставь глагол в правильную форму: {question['pronoun'].capitalize()} ({question['verb']['fi']})", reply_markup=builder.as_markup(resize_keyboard=True))
        await state.set_state(VerbStates.game_in_progress)

@verbs_router.message(StateFilter(VerbStates.game_in_progress))
async def check_end_answer(message: Message, state: FSMContext):
    if message.text == "Завершить игру" or game.inner_count == 10:
        await message.answer(f"Игра заверешна! Итоговый счёт: {game.correct_count}/{game.inner_count}")
        await show_game_menu(message, state)
        return

    answer = message.text.strip()
    correct_answer = game.get_answer()
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Завершить игру"))
    if game.check_conjuration(answer):
        await message.answer(f"✅ Верно!")
    else:
        highlighted = diff_answers(answer, correct_answer)
        await message.answer(
            f"❌ Неверно.\nТвой ответ с ошибками выделенными *звёздочками*:\n<code>{highlighted}</code>\n"
            f"Правильный ответ:\n<code>{correct_answer}</code>\nПопробуй следующий.",
            parse_mode="HTML",
            reply_markup=builder.as_markup(resize_keyboard=True)
        )
    question = game.new_word_question()
    await message.answer(f"Поставь глагол в правильную форму: {question['pronoun'].capitalize()} ({question['verb']['fi']})", reply_markup=builder.as_markup(resize_keyboard=True))

@verbs_router.message(StateFilter(VerbStates.choosing_difficulty))
async def check_word_to_word_answer(message: Message, state: FSMContext):
    text = message.text.strip()
    if message.text == "Завершить игру" or game.inner_count == 10:
        await message.answer(f"Игра заверешна! Итого количество ошибок: {game.incorrect_count}")
        await show_game_menu(message, state)
        return

    try:
        count = int(text.split()[0])
    except (ValueError, IndexError):
        await message.answer("Пожалуйста, выбери сложность из предложенных вариантов.")
        return
    data = await state.get_data()
    mode = data.get('mode', 'ru-fi')
    await state.update_data(verbs_count=count)
    question = game.new_quiz_question(count)
    correct_answer = question["correct_answer"]
    options = question["options"]
    await state.update_data(correct_verb=correct_answer)
    builder = ReplyKeyboardBuilder()
    for i in range(0, len(options), 4):
        builder.row(*[KeyboardButton(text=verb[mode[-2:]]) for verb in options[i:i + 4]])
    builder.row(KeyboardButton(text="Завершить игру"))
    await message.answer(
        f"Как переводится этот глагол? {correct_answer[mode[:2]].capitalize()}",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
    await state.set_state(VerbStates.word_to_word)

@verbs_router.message(StateFilter(VerbStates.word_to_word))
async def check_quiz_answer(message: Message, state: FSMContext):
    if message.text == "Завершить игру" or game.inner_count == 10:
        await message.answer(f"Игра заверешна! Итого количество ошибок: {game.incorrect_count}")
        await show_game_menu(message, state)
        return

    data = await state.get_data()
    count = data.get("verbs_count", 4)
    mode = data.get('mode', 'ru-fi')

    user_answer = message.text.strip()
    if game.check_answer(user_answer, mode[-2:]):
        question = game.new_quiz_question(count)
        correct_answer = question["correct_answer"]
        options = question["options"]
        await state.update_data(correct_verb=correct_answer)

        builder = ReplyKeyboardBuilder()
        for i in range(0, len(options), 4):
            builder.row(*[KeyboardButton(text=verb[mode[-2:]]) for verb in options[i:i + 4]])
        builder.row(KeyboardButton(text="Завершить игру"))

        await message.answer(
            f"✅ Верно!\n\nКак переводится этот глагол? {correct_answer[mode[:2]].capitalize()}",
            reply_markup=builder.as_markup(resize_keyboard=True)
        )
    else:
        await message.answer(
            f"❌ Неверно. Попробуй еще раз."
        )