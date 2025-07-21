import random
from db.db import get_table, DB_PATH
from games.base_game import BaseGame
from utils.nouns_class import NounWord, CASES

print(DB_PATH.resolve())
NOUNS = get_table('nouns')

class NounsGame(BaseGame):
    ITEMS = [dict(x) for x in NOUNS]

    def new_word_question(self, case: int = 0):
        self.inner_count += 1
        selected_noun = NounWord(random.choice(self.ITEMS))
        if case:
            selected_case = case
        else:
            selected_case = random.randint(1, 2)
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


