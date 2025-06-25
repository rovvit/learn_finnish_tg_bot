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
        KeyboardButton(text="Погода"),
        KeyboardButton(text="Время"),
    )
    builder.row(
        KeyboardButton(text="Глаголы"),
        KeyboardButton(text="Существительные")
    )
    await message.answer(
        '''
        Выбери во что играть.
        
        Числа - если хочешь проверить знания чисел
        Цвета - если хочешь проверить знания цветов
        Глаголы - если хочешь проверить знание глаголов и умение их склонять
        Погода - если хочешь проверить знания слов из темы "Погода"
        ''',
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
    await state.set_state(AppState.choosing_game_type)

def quiz_keyboard(options: list, key: str):
    builder = ReplyKeyboardBuilder()
    row = []
    for item in options:
        text = item[key]
        button = KeyboardButton(text=text)

        # Добавляем в текущий ряд, если текст короткий
        if len(text) <= 14:
            row.append(button)
            if len(row) == 4 and len(text) <= 7:
                builder.row(*row)
                row = []
            elif len(row) == 2 and len(text) > 7:
                builder.row(*row)
                row = []
        else:
            # если длинная кнопка — отправляем текущий ряд и добавляем её отдельно
            if row:
                builder.row(*row)
                row = []
            builder.row(button)

    # добавляем остатки
    if row:
        builder.row(*row)

    # завершить игру — последней строкой
    builder.row(KeyboardButton(text="Завершить игру"))
    return builder