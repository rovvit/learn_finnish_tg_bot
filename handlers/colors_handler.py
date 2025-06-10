from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from utils.ui import show_game_menu
from utils.diff_answer import diff_answers
from games.colors_game import ColorsGame
from states import AppState, ColorsStates

colors_router = Router()
game = ColorsGame()
MODES = {
    "EMOJI": "Выбор цвета по эмодзи",
    "EMOJI_TO_WORD": "Написать слово по эмодзи",
    "OTHER": "Другой режим (скоро)"
}

@colors_router.message(StateFilter(AppState.colors_game), F.text.casefold() == "цвета")
async def choose_mode(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=MODES["EMOJI"]),
        KeyboardButton(text=MODES["EMOJI_TO_WORD"]),
        KeyboardButton(text=MODES["OTHER"])
    )
    await message.answer("Выбери режим игры:", reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(ColorsStates.choosing_mode)

@colors_router.message(StateFilter(ColorsStates.choosing_mode))
async def choose_difficulty(message: Message, state: FSMContext):
    if message.text == MODES["EMOJI"]:
        await state.update_data(mode="emoji")
        builder = ReplyKeyboardBuilder()
        builder.row(
            KeyboardButton(text="4 цвета"),
            KeyboardButton(text="8 цветов"),
            KeyboardButton(text="12 цветов"),
            KeyboardButton(text="Завершить игру")
        )
        await message.answer("Правила игры: тебе будет задан цвет, тебе нужно будет выбрать правильный вариант.\nИгра идёт до 10 вопросов.\n\nВыбери уровень сложности:", reply_markup=builder.as_markup(resize_keyboard=True))
        await state.set_state(ColorsStates.choosing_difficulty_emoji)
    elif message.text == MODES["EMOJI_TO_WORD"]:
        await message.answer(
            "Отлично! Начинаем игру.\n\nПравила: необходимо написать заданный цвет на финнском",
            reply_markup=ReplyKeyboardRemove()
        )
        question = game.new_word_question()
        await state.set_state(ColorsStates.word_to_word)
        builder = ReplyKeyboardBuilder()
        builder.row(KeyboardButton(text="Завершить игру"))

        await message.answer(
            f"Как по-фински называется этот цвет? {question['emoji']} ({question['ru']})",
            reply_markup=builder.as_markup(resize_keyboard=True)
        )
    else:
        await message.answer("Этот режим пока в разработке.")

@colors_router.message(StateFilter(ColorsStates.choosing_difficulty_emoji))
async def color_quiz_emoji(message: Message, state: FSMContext):
    text = message.text.strip()
    if text == "Завершить игру" or game.inner_count == 10:
        await message.answer(f"Игра заверешна! Итого количество ошибок: {game.incorrect_count}")
        await show_game_menu(message, state)
        return

    try:
        count = int(text.split()[0])
    except (ValueError, IndexError):
        await message.answer("Пожалуйста, выбери сложность из предложенных вариантов.")
        return

    await state.update_data(color_count=count)
    question = game.new_quiz_question(count)
    correct_answer = question["correct_answer"]
    options = question["options"]

    builder = ReplyKeyboardBuilder()
    for i in range(0, len(options), 4):
        builder.row(*[KeyboardButton(text=color['fi']) for color in options[i:i+4]])
    builder.row(KeyboardButton(text="Завершить игру"))

    await message.answer(
        f"Какой это цвет? {correct_answer["emoji"]} ({correct_answer["ru"]})",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
    await state.set_state(ColorsStates.game_in_progress)

@colors_router.message(StateFilter(ColorsStates.game_in_progress))
async def check_quiz_answer(message: Message, state: FSMContext):
    if message.text == "Завершить игру" or game.inner_count == 10:
        await message.answer(f"Игра заверешна! Итого количество ошибок: {game.incorrect_count}")
        await show_game_menu(message, state)
        return

    data = await state.get_data()
    count = data.get("color_count", 4)

    user_answer = message.text.strip()
    if game.check_answer(user_answer, 'fi'):
        question = game.new_quiz_question(count)
        new_question = question["correct_answer"]
        options = question["options"]

        builder = ReplyKeyboardBuilder()
        for i in range(0, len(options), 4):
            builder.row(*[KeyboardButton(text=color['fi']) for color in options[i:i+4]])
        builder.row(KeyboardButton(text="Завершить игру"))

        await message.answer(
            f"✅ Верно!\n\nКакой это цвет? {new_question["emoji"]} ({new_question["ru"]})",
            reply_markup=builder.as_markup(resize_keyboard=True)
        )
    else:
        await message.answer(
            f"❌ Неверно. Попробуй еще раз."
        )

@colors_router.message(StateFilter(ColorsStates.word_to_word))
async def emoji_to_word_check(message: Message, state: FSMContext):
    if message.text == "Завершить игру":
        await show_game_menu(message, state)
        return

    answer = message.text.strip().lower()
    data = await state.get_data()
    correct_answer = data.get("correct_answer")

    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Завершить игру"))

    if game.check_answer(answer, 'fi'):
        await message.answer("✅ Верно!")
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
        new_question = game.new_word_question()
        await message.answer(f"Напиши цвет на финском: {new_question["ru"]} {new_question["emoji"]}", reply_markup=builder.as_markup(resize_keyboard=True))