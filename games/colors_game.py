import random

class ColorsGame:
    COLORS = [
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

    def __init__(self):
        self.correct_color = None

    def new_question(self, options_count: int = 4):
        options = random.sample(self.COLORS, k=options_count)
        self.correct_color = random.choice(options)
        return {
            "correct_answer": self.correct_color,
            "options": [color["fi"] for color in options],
        }

    def check_answer(self, answer: str) -> bool:
        return answer.lower().strip() == self.correct_color["fi"].lower().strip()
