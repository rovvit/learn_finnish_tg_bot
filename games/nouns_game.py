import random

from games.base_game import BaseGame
from utils.nouns_class import NounWord, CASES

NOUNS = [
    {'fi': 'avain', 'ru': 'ключ', 'isFinnish': True},
    {'fi': 'ikkuna', 'ru': 'окно', 'isFinnish': True},
    {'fi': 'kahvitauko', 'ru': 'кофе-брейк', 'isFinnish': True},
    {'fi': 'kahvi', 'ru': 'кофе', 'isFinnish': False},
    {'fi': 'kello', 'ru': 'часы (время)', 'isFinnish': True},
    {'fi': 'kirja', 'ru': 'книга', 'isFinnish': True},
    {'fi': 'kotitehtävä', 'ru': 'домашнее задание', 'isFinnish': True},
    {'fi': 'kurssi', 'ru': 'курс', 'isFinnish': False},
    {'fi': 'kysymys', 'ru': 'вопрос', 'isFinnish': True},
    {'fi': 'lamppu', 'ru': 'лампа', 'isFinnish': False},
    {'fi': 'läppäri', 'ru': 'ноутбук', 'isFinnish': False},
    {'fi': 'opettaja', 'ru': 'учитель', 'isFinnish': True},
    {'fi': 'opiskelija', 'ru': 'ученик', 'isFinnish': True},
    {'fi': 'oppikirja', 'ru': 'учебник', 'isFinnish': True},
    {'fi': 'ovi', 'ru': 'дверь', 'isFinnish': True},
    {'fi': 'puhelin', 'ru': 'телефон', 'isFinnish': True},
    {'fi': 'pöytä', 'ru': 'стол', 'isFinnish': True},
    {'fi': 'sanakirja', 'ru': 'словарь', 'isFinnish': True},
    {'fi': 'tietokone', 'ru': 'компьютер', 'isFinnish': True},
    {'fi': 'tuoli', 'ru': 'стул', 'isFinnish': False},
    {'fi': 'valo', 'ru': 'свет', 'isFinnish': True},
    {'fi': 'ovi', 'ru': 'дверь', 'isFinnish': True},
    {'fi': 'ovi', 'ru': 'дверь', 'isFinnish': True},
]
class NounsGame(BaseGame):
    ITEMS = NOUNS

    def new_word_question(self):
        self.inner_count += 1
        selected_noun = NounWord(random.choice(self.ITEMS))
        selected_case = random.randint(1, 1)
        answer = selected_noun.inflict(selected_case)
        self.correct_answer = answer
        return {
            'answer': answer,
            'word': selected_noun,
            'case': CASES[selected_case]
        }

    def check_infliction(self, answer: str) -> bool:
        if answer.lower().strip() == self.correct_answer.lower().strip():
            self.correct_count += 1
        else:
            self.incorrect_count += 1
        return answer.lower().strip() == self.correct_answer.lower().strip()


