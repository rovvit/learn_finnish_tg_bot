import random

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton

from games.clock_game import ClockGame
from states import AppState, ClockStates
from utils.ui import show_game_menu

clock_router = Router()

@clock_router.message(StateFilter(AppState.clock_game), F.text.casefold() == "время")
async def start_game(message: Message, state: FSMContext):
    game = ClockGame()
    await state.update_data(game=game)
    question = game.new_clock_question()
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Завершить игру"))
    await message.answer_photo(
        photo=BufferedInputFile(question['img'].read(), filename="clock.png"),
        caption=f"🕒 Paljonko kello se on? ({question['hour']:02d}:{question['minute']:02d})",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
    await state.set_state(ClockStates.game_in_progress)


@clock_router.message(StateFilter(ClockStates.game_in_progress))
async def check_answer(message: Message, state: FSMContext):
    text = message.text.strip()
    data = await state.get_data()
    game: ClockGame = data.get("game")

    if text == "Завершить игру" or game.inner_count == 10:
        await message.answer(f"Игра заверешна! Итого количество ошибок: {game.incorrect_count}")
        await show_game_menu(message, state)
        return

    if game.check_clock_answer(text):
        new_question = game.new_clock_question()
        await message.answer("✅ Верно!")
        await message.answer_photo(
            photo=BufferedInputFile(new_question['img'].read(), filename="clock.png"),
            caption=f"🕒 Paljonko kello se on? ({new_question['hour']:02d}:{new_question['minute']:02d})"
        )
    else:
        await message.answer("❌ Где-то закралась ошибка, попробуй ещё раз")
