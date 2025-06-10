import random

class BaseGame():
    ITEMS = []

    def __init__(self):
        self.correct_answer = None

    def get_answer(self):
        return self.correct_answer

    def new_quiz_question(self, options_count: int = 4):
        options = random.sample(self.ITEMS, k=options_count)
        self.correct_answer = random.choice(options)
        return {
            "correct_answer": self.correct_answer,
            "options": [item for item in options],
        }

    def new_word_question(self):
        self.correct_answer = random.choice(self.ITEMS)
        return self.correct_answer

    def check_answer(self, answer: str, key: str = 'fi') -> bool:
        return answer.lower().strip() == self.correct_answer[key].lower().strip()