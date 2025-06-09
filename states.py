from aiogram.fsm.state import StatesGroup, State

class AppState(StatesGroup):
    choosing_game_type = State()
    choosing_game_subtype = State()
    game_in_progress = State()
    numbers_game_in_progress = State()