# utils/ui.py
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from states import AppState

async def show_game_menu(message: Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Числа"),
        KeyboardButton(text="Цвета"),
        KeyboardButton(text="Глаголы")
    )
    await message.answer(
        "Выбери во что играть",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
    await state.set_state(AppState.choosing_game_type)