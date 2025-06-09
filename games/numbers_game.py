from num2words import num2words
from random import randint

class NumbersGame:
    def __init__(self):
        self.current_number = None

    def new_question(self, max_number=100):
        self.current_number = randint(1, max_number)
        return self.current_number

    def check_answer(self, answer: str) -> bool:
        if self.current_number is None:
            return False
        correct = num2words(self.current_number, lang='fi')
        return answer.strip().lower() == correct.strip().lower()

    def get_correct_answer(self) -> str:
        if self.current_number is None:
            return ""
        return num2words(self.current_number, lang='fi')
