from num2words import num2words
from random import randint

from games.base_game import BaseGame


class NumbersGame(BaseGame):
    def new_question(self, max_number: int = 100):
        self.inner_count += 1
        self.correct_answer = randint(1, max_number)
        return self.correct_answer

    def check_answer(self, answer: str, *kwargs) -> bool:
        if self.correct_answer is None:
            return False
        correct = num2words(self.correct_answer, lang='fi')
        if answer.strip().lower() == correct.strip().lower():
            self.correct_count += 1
        else:
            self.incorrect_count += 1
        return answer.strip().lower() == correct.strip().lower()

    def get_correct_answer(self) -> str:
        if self.correct_answer is None:
            return ""
        return num2words(self.correct_answer, lang='fi')
