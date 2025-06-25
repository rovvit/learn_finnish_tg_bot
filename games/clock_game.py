import random
from num2words import num2words
from games.base_game import BaseGame
from utils.clock_drawer import generate_clock


class ClockGame(BaseGame):
    def __init__(self):
        super().__init__()
        self.hour = 0
        self.minute = 0

    def new_clock_question(self):
        self.hour = random.randint(0, 23)
        self.minute = random.choices(
            population=list(range(60)),
            weights=[10 if m in {0, 15, 30, 45} else 1 for m in range(60)]
        )[0]
        self.clock_image = generate_clock(self.hour, self.minute)

        return {
            'hour': self.hour,
            'minute': self.minute,
            'img': self.clock_image
        }

    def check_clock_answer(self, answer: str) -> bool:
        hours = [self.hour, self.hour + 12, self.hour - 12]
        text_hours = [num2words(h, lang='fi') for h in hours if (h > 0) and (h < 24)]
        stripped_ans = ' '.join(answer.strip().split()).lower()
        if self.minute == 0:
            correct_answers = [f"tasan {text_hour}" for text_hour in text_hours]
        else:
            correct_answers = [
                                  f"{text_hour} {num2words(self.minute, lang='fi')}" for text_hour in text_hours
                              ] + [
                                  f"{num2words(self.minute, lang='fi')} yli {text_hour}" for text_hour in text_hours]
            if self.minute == 30:
                for h in hours:
                    correct_answers.append(f"puoli {num2words(h + 1 % 12, lang='fi')}")
            if self.minute == 15:
                for h in text_hours:
                    correct_answers.append(f"värtti yli {h}")
            if self.minute == 45:
                for h in hours:
                    correct_answers.append(f"värtti vaille {num2words(h + 1 % 12, lang='fi')}")
            if self.minute > 30:
                for h in hours:
                    correct_answers.append(
                        f"{num2words(60 - self.minute, lang='fi')} vaille {num2words(h + 1 % 12, lang='fi')}")

        is_correct = any(correct_answer in stripped_ans for correct_answer in correct_answers)
        print(correct_answers)
        if is_correct:
            self.correct_count += 1
        else:
            self.incorrect_count += 1
        return is_correct