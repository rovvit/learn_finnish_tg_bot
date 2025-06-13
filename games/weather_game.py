from games.base_game import BaseGame

WEATHER = [
    {'ru': 'Солнечно', 'fi': 'Aurinkoinen', 'emoji': '☀️'},
    {'ru': 'Облачно', 'fi': 'Pilvinen', 'emoji': '☁️'},
    {'ru': 'Дождь', 'fi': 'Sade', 'emoji': '🌧'},
    {'ru': 'Гроза', 'fi': 'Ukkosta', 'emoji': '⛈'},
    {'ru': 'Молния', 'fi': 'Salamaa', 'emoji': '⚡️'},
    {'ru': 'Радуга', 'fi': 'Sateenkaari', 'emoji': '🌈'},
    {'ru': 'Мороз', 'fi': 'Pakkasta', 'emoji': '🥶'},
    {'ru': 'Снег', 'fi': 'Lumi', 'emoji': '❄️'},
    {'ru': 'Жара', 'fi': 'Helle', 'emoji': '🥵'},
    {'ru': 'Ветренно', 'fi': 'Tuulinen', 'emoji': '🌬'},
    {'ru': 'Горячо', 'fi': 'Kuuma', 'emoji': '☀️'},
    {'ru': 'Холодно', 'fi': 'Kylmä', 'emoji': '🥶'},
    {'ru': 'Туманно', 'fi': 'Sumuinen', 'emoji': '🌫'},
    {'ru': 'Шторм', 'fi': 'Myrsky', 'emoji': '⛈'},
]


class WeatherGame(BaseGame):
    ITEMS = WEATHER