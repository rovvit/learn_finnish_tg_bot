from num2words import num2words
from random import randint
import difflib

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

    def diff_answers(self, user_answer: str, correct_answer: str) -> str:
        seqm = difflib.SequenceMatcher(None, user_answer.lower(), correct_answer.lower())
        result = []
        for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
            text = user_answer[a0:a1]
            if opcode == 'equal':
                result.append(text)
            elif opcode == 'replace' or opcode == 'delete':
                # Выделяем ошибочные участки звездочками
                result.append(f"*{text}*")
            elif opcode == 'insert':
                # Показываем пропущенный текст из правильного ответа
                inserted = correct_answer[b0:b1]
                result.append(f"[+{inserted}+]")
        return "".join(result)