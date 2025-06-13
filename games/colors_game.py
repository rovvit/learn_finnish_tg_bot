import random

from games.base_game import BaseGame



class ColorsGame(BaseGame):
    ITEMS = [
        {"emoji": "🔴", "ru": "красный", "fi": "punainen"},
        {"emoji": "🟠", "ru": "оранжевый", "fi": "oranssi"},
        {"emoji": "🟡", "ru": "жёлтый", "fi": "keltainen"},
        {"emoji": "🟢", "ru": "зелёный", "fi": "vihreä"},
        {"emoji": "🔵", "ru": "синий", "fi": "sininen"},
        {"emoji": "🔷", "ru": "голубой", "fi": "vaaleansininen"},
        {"emoji": "🟣", "ru": "фиолетовый", "fi": "violetti"},
        {"emoji": "⚫", "ru": "чёрный", "fi": "musta"},
        {"emoji": "⚪", "ru": "белый", "fi": "valkoinen"},
        {"emoji": "🟤", "ru": "коричневый", "fi": "ruskea"},
        {"emoji": "🌸", "ru": "розовый", "fi": "vaaleanpunainen"},
        {"emoji": "🍋‍🟩", "ru": "лаймовый", "fi": "limenvihreä"},
        {"emoji": "🥇", "ru": "золотой", "fi": "kultainen"},
        {"emoji": "💜", "ru": "лиловый", "fi": "liila"},
        {"emoji": "🍑", "ru": "персиковый", "fi": "persikka"},
        {"emoji": "🍒", "ru": "вишнёвый", "fi": "kirsikanpunainen"},
        {"emoji": "🫒", "ru": "оливковый", "fi": "oliivi"},
        {"emoji": "🧊", "ru": "ледяной", "fi": "jääsininen"},
        {"emoji": "🌰", "ru": "каштановый", "fi": "kastanja"},
        {"emoji": "🌕", "ru": "кремовый", "fi": "kerma"},
        {"emoji": "🩶", "ru": "серый", "fi": "harmaa"},
    ]
