from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from utils.ui import show_game_menu
from games.colors_game import ColorsGame
from states import AppState, ColorsStates

colors_router = Router()
game = ColorsGame()

@colors_router.message(StateFilter(AppState.colors_game), F.text.casefold() == "цвета")
async def choose_mode(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Выбор цвета по эмодзи"),
        KeyboardButton(text="Другой режим (скоро)")
    )
    await message.answer("Выбери режим игры:", reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(ColorsStates.choosing_mode)

@colors_router.message(StateFilter(ColorsStates.choosing_mode))
async def choose_difficulty(message: Message, state: FSMContext):
    if message.text == "Выбор цвета по эмодзи":
        await state.update_data(mode="emoji_to_word")
        builder = ReplyKeyboardBuilder()
        builder.row(
            KeyboardButton(text="4 цвета"),
            KeyboardButton(text="8 цветов"),
            KeyboardButton(text="12 цветов"),
            KeyboardButton(text="Завершить игру")
        )
        await message.answer("Выбери уровень сложности:", reply_markup=builder.as_markup(resize_keyboard=True))
        await state.set_state(ColorsStates.choosing_difficulty)
    else:
        await message.answer("Этот режим пока в разработке.")

@colors_router.message(StateFilter(ColorsStates.choosing_difficulty))
async def start_game_or_stop(message: Message, state: FSMContext):
    text = message.text.strip()
    if text == "Завершить игру":
        await show_game_menu(message, state)
        return

    try:
        count = int(text.split()[0])
    except (ValueError, IndexError):
        await message.answer("Пожалуйста, выбери сложность из предложенных вариантов.")
        return

    await state.update_data(color_count=count)
    question = game.new_question(count)
    correct_answer = question["correct_answer"]
    options = question["options"]
    await state.update_data(correct_color=correct_answer["fi"])

    builder = ReplyKeyboardBuilder()
    for i in range(0, len(options), 4):
        builder.row(*[KeyboardButton(text=color) for color in options[i:i+4]])
    builder.row(KeyboardButton(text="Завершить игру"))

    await message.answer(
        f"Какой это цвет? {correct_answer["emoji"]} ({correct_answer["ru"]})",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
    await state.set_state(ColorsStates.game_in_progress)

@colors_router.message(StateFilter(ColorsStates.game_in_progress))
async def check_answer(message: Message, state: FSMContext):
    if message.text == "Завершить игру":
        await show_game_menu(message, state)
        return

    data = await state.get_data()
    correct_answer = data.get("correct_color")
    count = data.get("color_count", 4)

    user_answer = message.text.strip()

    if user_answer == correct_answer:
        question = game.new_question(count)
        correct_answer = question["correct_answer"]
        options = question["options"]
        await state.update_data(correct_color=correct_answer["fi"])

        builder = ReplyKeyboardBuilder()
        for i in range(0, len(options), 4):
            builder.row(*[KeyboardButton(text=color) for color in options[i:i+4]])
        builder.row(KeyboardButton(text="Завершить игру"))

        await message.answer(
            f"✅ Верно!\n\nКакой это цвет? {correct_answer["emoji"]} ({correct_answer["ru"]})",
            reply_markup=builder.as_markup(resize_keyboard=True)
        )
    else:
        await message.answer(
            f"❌ Неверно. Попробуй еще раз."
        )