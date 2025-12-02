from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from games.weather_game import WeatherGame
from states import AppState, WeatherStates
from utils.ui import show_game_menu

weather_router = Router()

MODES = {
    'choose_one_fi_ru': 'Выбор перевода (FI-RU)',
    'choose_one_ru_fi': 'Выбор перевода (RU-FI)'
}


@weather_router.message(StateFilter(AppState.weather_game), F.text.casefold() == "погода")
async def choose_mode(message: Message, state: FSMContext):
    game = WeatherGame()
    await state.update_data(game=game)
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=MODES['choose_one_ru_fi']),
        KeyboardButton(text=MODES['choose_one_fi_ru'])
    )
    builder.row(
        KeyboardButton(text="Завершить игру")
    )
    await message.answer("Выбери режим игры:", reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(WeatherStates.choosing_mode)


@weather_router.message(StateFilter(WeatherStates.choosing_mode))
async def start_game_or_stop(message: Message, state: FSMContext):
    data = await state.get_data()
    game: WeatherGame = data.get("game")
    if message.text == "Завершить игру":
        await state.set_state(AppState.choosing_game_type)
        await show_game_menu(message, state)
        return

    if message.text == MODES['choose_one_ru_fi']:
        await message.answer(
            "Отлично! Начинаем игру.",
            reply_markup=ReplyKeyboardRemove()
        )
        builder = ReplyKeyboardBuilder()
        mode = 'ru-fi'
        await state.update_data(mode=mode)
        await message.answer(
            f"Правила: тебе будет загадано слово, нужно будет выбрать, какой перевод правильный.\nИгра идёт до 10 вопросов.",
            reply_markup=builder.as_markup(resize_keyboard=True))
        question = game.new_quiz_question(4)
        correct_answer = question["correct_answer"]
        options = question["options"]
        await state.update_data(correct_verb=correct_answer)
        builder = ReplyKeyboardBuilder()
        for i in range(0, len(options), 4):
            builder.row(*[KeyboardButton(text=verb[mode[-2:]]) for verb in options[i:i + 4]])
        builder.row(KeyboardButton(text="Завершить игру"))
        await message.answer(
            f"Как переводится это слово? {correct_answer[mode[:2]].capitalize()} {correct_answer['emoji']}",
            reply_markup=builder.as_markup(resize_keyboard=True)
        )
        await state.set_state(WeatherStates.game_in_progress)

    if message.text == MODES['choose_one_fi_ru']:
        await message.answer(
            "Отлично! Начинаем игру.",
            reply_markup=ReplyKeyboardRemove()
        )
        builder = ReplyKeyboardBuilder()
        mode = 'fi-ru'
        await state.update_data(mode=mode)
        await message.answer(
            f"Правила: тебе будет загадано слово, нужно будет выбрать, какой перевод правильный.\nИгра идёт до 10 вопросов.",
            reply_markup=builder.as_markup(resize_keyboard=True))
        question = game.new_quiz_question(4)
        correct_answer = question["correct_answer"]
        options = question["options"]
        await state.update_data(correct_verb=correct_answer)
        builder = ReplyKeyboardBuilder()
        for i in range(0, len(options), 4):
            builder.row(*[KeyboardButton(text=verb[mode[-2:]]) for verb in options[i:i + 4]])
        builder.row(KeyboardButton(text="Завершить игру"))
        await message.answer(
            f"Как переводится это слово? {correct_answer[mode[:2]].capitalize()} {correct_answer['emoji']}",
            reply_markup=builder.as_markup(resize_keyboard=True)
        )
        await state.set_state(WeatherStates.game_in_progress)


@weather_router.message(StateFilter(WeatherStates.game_in_progress))
async def check_word_to_word_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    game: WeatherGame = data.get("game")
    text = message.text.strip()
    if text == "Завершить игру" or game.inner_count == 10:
        await message.answer(f"Игра завершена! Итого количество ошибок: {game.incorrect_count}")
        await show_game_menu(message, state)
        return

    data = await state.get_data()
    mode = data.get('mode', 'ru-fi')
    await state.update_data(verbs_count=4)

    if game.check_answer(text, mode[-2:]):
        question = game.new_quiz_question(4)
        correct_answer = question["correct_answer"]
        options = question["options"]
        await state.update_data(correct_verb=correct_answer)

        builder = ReplyKeyboardBuilder()
        for i in range(0, len(options), 4):
            builder.row(*[KeyboardButton(text=verb[mode[-2:]]) for verb in options[i:i + 4]])
        builder.row(KeyboardButton(text="Завершить игру"))

        await message.answer(
            f"✅ Верно!\n\nКак переводится это слово? {correct_answer[mode[:2]].capitalize()} {correct_answer['emoji']}",
            reply_markup=builder.as_markup(resize_keyboard=True)
        )
    else:
        await message.answer(
            f"❌ Неверно. Попробуй еще раз."
        )
