from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from games.nouns_game import NounsGame
from states import AppState, NounsStates
from utils.ui import show_game_menu, quiz_keyboard
from utils.diff_answer import diff_answers

nouns_router = Router()

MODES = {
    'infliction': 'Склонять',
    'choose_one_fi_ru': 'Выбор перевода (FI-RU)',
    'choose_one_ru_fi': 'Выбор перевода (RU-FI)'
}


@nouns_router.message(StateFilter(AppState.nouns_game), F.text.casefold() == "существительные")
async def choose_mode(message: Message, state: FSMContext):
    game = NounsGame()
    await state.update_data(game=game)
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=MODES['infliction']),
    )
    builder.row(
        KeyboardButton(text=MODES['choose_one_ru_fi']),
        KeyboardButton(text=MODES['choose_one_fi_ru'])
    )
    builder.row(
        KeyboardButton(text="Завершить игру")
    )
    await message.answer("Выбери режим игры:", reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(NounsStates.choosing_mode)


@nouns_router.message(StateFilter(NounsStates.choosing_mode))
async def start_end_game_or_stop(message: Message, state: FSMContext):
    data = await state.get_data()
    game: NounsGame = data.get("game")
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
        )
        builder.row(
            KeyboardButton(text="Завершить игру")
        )
        await state.update_data(mode='ru-fi')
        await message.answer(
            f"Выбери количество вариантов:",
            reply_markup=builder.as_markup(resize_keyboard=True))
        await state.set_state(NounsStates.choosing_difficulty)
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
        )
        builder.row(
            KeyboardButton(text="Завершить игру")
        )
        await state.update_data(mode='fi-ru')
        await message.answer(
            f"Правила: тебе будет загадано слово, нужно будет выбрать, какой перевод правильный.\nИгра идёт до 10 вопросов.\n\nВыбери количество вариантов:",
            reply_markup=builder.as_markup(resize_keyboard=True))
        await state.set_state(NounsStates.choosing_difficulty)
    if message.text == MODES['infliction']:
        await message.answer(
            "Отлично! Начинаем игру.",
            reply_markup=ReplyKeyboardRemove()
        )
        builder = ReplyKeyboardBuilder()
        builder.row(KeyboardButton(text="Завершить игру"))
        question = game.new_word_question()

        await message.answer(
            f"Поставь слово в правильную форму: {question['case']['q_nonpers'].capitalize()} ({question['word'].fi.capitalize()})? ",
            reply_markup=builder.as_markup(resize_keyboard=True))
        await state.set_state(NounsStates.game_in_progress)


@nouns_router.message(StateFilter(NounsStates.game_in_progress))
async def check_end_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    game: NounsGame = data.get("game")
    if message.text == "Завершить игру" or game.inner_count == 10:
        await message.answer(f"Игра заверешна! Итоговый счёт: {game.correct_count}/{game.inner_count}")
        await show_game_menu(message, state)
        return

    answer = message.text.strip()
    correct_answer = game.get_answer()
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Завершить игру"))
    if game.check_infliction(answer):
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
    await message.answer(
        f"Поставь слово в правильную форму: {question['case']['q_nonpers'].capitalize()} ({question['word'].fi.capitalize()})? ")


@nouns_router.message(StateFilter(NounsStates.choosing_difficulty))
async def check_word_to_word_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    game: NounsGame = data.get("game")
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
    await state.update_data(answers=count)
    question = game.new_quiz_question(count)
    correct_answer = question["correct_answer"]
    options = question["options"]
    await state.update_data(correct_verb=correct_answer)
    builder = quiz_keyboard(options, mode[-2:])
    await message.answer(
        f"Как переводится это слово? {correct_answer[mode[:2]].capitalize()}",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
    await state.set_state(NounsStates.word_to_word)


@nouns_router.message(StateFilter(NounsStates.word_to_word))
async def check_quiz_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    game: NounsGame = data.get("game")
    if message.text == "Завершить игру" or game.inner_count == 10:
        await message.answer(f"Игра заверешна! Итого количество ошибок: {game.incorrect_count}")
        await show_game_menu(message, state)
        return

    data = await state.get_data()
    count = data.get("answers", 4)
    mode = data.get('mode', 'ru-fi')

    user_answer = message.text.strip()
    if game.check_answer(user_answer, mode[-2:]):
        question = game.new_quiz_question(count)
        correct_answer = question["correct_answer"]
        options = question["options"]
        await state.update_data(correct_verb=correct_answer)

        builder = quiz_keyboard(options, mode[-2:])
        await message.answer(
            f"✅ Верно!\n\nКак переводится этот глагол? {correct_answer[mode[:2]].capitalize()}",
            reply_markup=builder.as_markup(resize_keyboard=True)
        )
    else:
        await message.answer(
            f"❌ Неверно. Попробуй еще раз."
        )
