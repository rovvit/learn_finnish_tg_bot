from aiogram.fsm.state import State, StatesGroup

class AppState(StatesGroup):
    choosing_game_type = State()
    numbers_game = State()
    colors_game = State()
    verbs_game = State()
    weather_game = State()
    nouns_game = State()

class NumbersStates(StatesGroup):
    choosing_difficulty = State()
    game_in_progress = State()

class ColorsStates(StatesGroup):
    choosing_mode = State()
    choosing_difficulty_emoji = State()
    game_in_progress = State()
    word_to_word = State()

class VerbStates(StatesGroup):
    choosing_mode = State()
    game_in_progress = State()
    choosing_difficulty = State()
    word_to_word = State()

class WeatherStates(StatesGroup):
    game_in_progress = State()
    word_to_word = State()
    choosing_mode = State()

class NounsStates(StatesGroup):
    choosing_mode = State()
    game_in_progress = State()
    choosing_difficulty = State()
    word_to_word = State()