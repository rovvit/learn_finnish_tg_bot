import random

from db.models import Verb
from games.base_game import BaseGame
from utils.KPT_transform import KPT_transform


def make_end_for_third_person(verb_base: str, plural=False) -> str:
    if plural:
        if 'a' in verb_base or 'o' in verb_base or 'u' in verb_base:
            return 'vat'
        return 'vät'
    if verb_base.endswith('aa') or verb_base.endswith('ää') or verb_base.endswith('uo'):
        return ''
    return verb_base[-1]


class VerbGame(BaseGame):

    PRONOUNS = {
        1: {'pronoun': 'minä', 'ending': 'n', 'negative': 'en'},
        2: {'pronoun': 'sinä', 'ending': 't', 'negative': 'et'},
        3: {'pronoun': 'hän', 'negative': 'ei'},
        4: {'pronoun': 'me', 'ending': 'mme', 'negative': 'emme'},
        5: {'pronoun': 'te', 'ending': 'tte', 'negative': 'ette'},
        6: {'pronoun': 'he', 'negative': 'eivät'}
    }

    EXCEPTIONS = {
        'JUOSTA': {
            1: 'juoksen',
            2: 'juokset',
            3: 'juoksee',
            4: 'juoksemme',
            5: 'juoksette',
            6: 'juoksevat'
        },
        'NAHDA': {
            1: 'näen',
            2: 'näet',
            3: 'näkee',
            4: 'näemme',
            5: 'näette',
            6: 'näkevät'
        },
        'TEHDA': {
            1: 'teen',
            2: 'teet',
            3: 'tekee',
            4: 'teemme',
            5: 'teette',
            6: 'tekevät'
        },
        'OLLA': {
            1: 'olen',
            2: 'olet',
            3: 'on',
            4: 'olemme',
            5: 'olette',
            6: 'ovat'
        }
    }

    async def new_word_question(self):
        self.inner_count += 1

        verb = await Verb.get_random()
        selected_verb = {
            "id": verb.id,
            "ru": verb.ru,
            "fi": verb.fi,
            "type": verb.type,
            "base": verb.base,
        }

        selected_pronoun = random.randint(1, 6)
        answer = self.conjure_verb(selected_verb, selected_pronoun)
        self.correct_answer = answer
        return {
            'answer': answer,
            'verb': selected_verb,
            'pronoun': self.PRONOUNS[selected_pronoun]['pronoun']
        }

    def check_conjuration(self, answer: str) -> bool:
        if answer.lower().strip() == self.correct_answer.lower().strip():
            self.correct_count += 1
        else:
            self.incorrect_count += 1
        return answer.lower().strip() == self.correct_answer.lower().strip()

    def conjure_verb(self, verb_obj, pronoun=1) -> str:
        verb = verb_obj['fi']
        if verb.lower() == 'tehdä':
            return self.EXCEPTIONS['TEHDA'][pronoun]
        if verb.lower() == 'nähdä':
            return self.EXCEPTIONS['NAHDA'][pronoun]
        if verb.lower() == 'juosta':
            return self.EXCEPTIONS['JUOSTA'][pronoun]
        if verb.lower() == 'olla':
            return self.EXCEPTIONS['OLLA'][pronoun]

        match verb_obj['type']:
            case 1:
                verb_base = KPT_transform(verb[:-1])
            case 2:
                verb_base = verb[:-2]
            case 3:
                verb_base = verb[:-2]
                verb_base = verb_base + 'e'
            case 4:
                verb_base = verb[:-2]
                if 'a' in verb_base or 'o' in verb_base or 'u' in verb_base:
                    verb_base = verb_base + 'a'
                else:
                    verb_base = verb_base + 'ä'
            case 5:
                verb_base = verb[:-2]
                verb_base = verb_base + 'tse'
            case 6:
                verb_base = verb[:-2]
                verb_base = verb_base + 'ne'
            case _:
                raise Exception('There is no such verb type!')

        if pronoun == 3:
            return verb_base + make_end_for_third_person(verb_base)
        if pronoun == 6:
            return verb_base + make_end_for_third_person(verb_base, True)
        return verb_base + self.PRONOUNS[pronoun]['ending']

