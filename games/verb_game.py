import random

class VerbGame:
    VERBS = [
        {'ru': 'быть', 'fi': 'olla', 'type': 3},
        {'ru': 'кушать', 'fi': 'syödä', 'type': 2},
        {'ru': 'жить', 'fi': 'asua', 'type': 1},
        {'ru': 'просыпаться', 'fi': 'herätä', 'type': 4},
        {'ru': 'выбирать', 'fi': 'valita', 'type': 5},
        {'ru': 'сидеть', 'fi': 'istua', 'type': 1},
        {'ru': 'стоять', 'fi': 'seisoa', 'type': 1},
        {'ru': 'пить', 'fi': 'juoda', 'type': 2},
        {'ru': 'понимать', 'fi': 'ymmärtää', 'type': 1},
        {'ru': 'помнить', 'fi': 'muistaa', 'type': 1},
        {'ru': 'забыть', 'fi': 'unohtaa', 'type': 1},
        {'ru': 'думать', 'fi': 'ajatella', 'type': 3},
        {'ru': 'знать', 'fi': 'tietää', 'type': 1},
        {'ru': 'уметь, знать', 'fi': 'osata', 'type': 4},
        {'ru': 'учиться', 'fi': 'opiskella', 'type': 3},
        {'ru': 'учиться', 'fi': 'oppia', 'type': 1},
        {'ru': 'спрашивать', 'fi': 'kysyä', 'type': 1},
        {'ru': 'запрашивать', 'fi': 'pyytää', 'type': 1},
        {'ru': 'сказать', 'fi': 'sanoa', 'type': 1},
        {'ru': 'рассказывать', 'fi': 'kertoa', 'type': 1},
        {'ru': 'разговаривать', 'fi': 'keskustella', 'type': 3},
        {'ru': 'спать', 'fi': 'nukkua', 'type': 1},
        {'ru': 'вставать', 'fi': 'nousta', 'type': 3},
        {'ru': 'врать', 'fi': 'maata', 'type': 4},
        {'ru': 'мыть', 'fi': 'pestä', 'type': 3},
        {'ru': 'мыть (посуду)', 'fi': 'tiskata', 'type': 4},
        {'ru': 'убираться', 'fi': 'siivota', 'type': 4},
        {'ru': 'пылесосить', 'fi': 'imuroida', 'type': 2},
        {'ru': 'плавать', 'fi': 'uida', 'type': 2},
        {'ru': 'гулять', 'fi': 'kävellä', 'type': 3},
        {'ru': 'кататься на велосипеде', 'fi': 'pyöräillä', 'type': 3},
        {'ru': 'водить', 'fi': 'ajaa', 'type': 1},
        {'ru': 'бежать', 'fi': 'juosta', 'type': 3},
        {'ru': 'играть (про спорт)', 'fi': 'pelata', 'type': 4},
        {'ru': 'играть (про детей)', 'fi': 'leikkiä', 'type': 1},
        {'ru': 'звать', 'fi': 'soittaa', 'type': 1},
        {'ru': 'брать', 'fi': 'ottaa', 'type': 1},
        {'ru': 'давать', 'fi': 'antaa', 'type': 1},
        {'ru': 'одолжить', 'fi': 'lainata', 'type': 4},
        {'ru': 'встретить', 'fi': 'tavata', 'type': 4},
        {'ru': 'знакомиться', 'fi': 'tutustua', 'type': 1},
        {'ru': 'делать', 'fi': 'tehdä', 'type': 2},
        {'ru': 'видеть', 'fi': 'nähdä', 'type': 2},
        {'ru': 'смотреть', 'fi': 'katsoa', 'type': 1},
        {'ru': 'прийти', 'fi': 'tulla', 'type': 3},
        {'ru': 'идти', 'fi': 'mennä', 'type': 3},
        {'ru': 'уйти', 'fi': 'lähteä', 'type': 1},
        {'ru': 'оставаться', 'fi': 'jäädä', 'type': 2},
        {'ru': 'приезжать', 'fi': 'saapua', 'type': 1},
        {'ru': 'посещать', 'fi': 'käydä', 'type': 2},
        {'ru': 'приносить', 'fi': 'tuoda', 'type': 2},
        {'ru': 'нести', 'fi': 'viedä', 'type': 2},
        {'ru': 'любить', 'fi': 'rakastaa', 'type': 1},
        {'ru': 'ненавидеть', 'fi': 'vihata', 'type': 4},
        {'ru': 'любить(навиться)', 'fi': 'tykätä', 'type': 4},
        {'ru': 'бояться', 'fi': 'pelätä', 'type': 4},
        {'ru': 'одеваться', 'fi': 'pukea', 'type': 1},
        {'ru': 'раздеваться', 'fi': 'riisua', 'type': 1},
        {'ru': 'платить', 'fi': 'maksaa', 'type': 1},
        {'ru': 'покупать', 'fi': 'ostaa', 'type': 1},
        {'ru': 'продавать', 'fi': 'myydä', 'type': 2},
        {'ru': 'писать', 'fi': 'kirjoittaa', 'type': 1},
        {'ru': 'читать', 'fi': 'lukea', 'type': 1},
        {'ru': 'слушать', 'fi': 'kuunnella', 'type': 3},
        {'ru': 'слышать', 'fi': 'kuulla', 'type': 3},
        {'ru': 'рисовать', 'fi': 'piirtää', 'type': 1},
        {'ru': 'красить', 'fi': 'maalata', 'type': 4},
        {'ru': 'смеяться', 'fi': 'nauraa', 'type': 1},
        {'ru': 'плакать', 'fi': 'itkeä', 'type': 1},
        {'ru': 'улыбаться', 'fi': 'hymyillä', 'type': 3},
        {'ru': 'путешествовать', 'fi': 'matkustaa', 'type': 1},
        {'ru': 'переезжать', 'fi': 'muuttaa', 'type': 1},
        {'ru': 'толкать', 'fi': 'työntää', 'type': 1},
        {'ru': 'тянуть', 'fi': 'vetää', 'type': 1},
        {'ru': 'поднимать', 'fi': 'nostaa', 'type': 1},
        {'ru': 'считать', 'fi': 'laskea', 'type': 1},
        {'ru': 'помещать', 'fi': 'laittaa', 'type': 1},
        {'ru': 'бросать', 'fi': 'heittää', 'type': 1},
        {'ru': 'беспокоить', 'fi': 'häiritä', 'type': 5},
        {'ru': 'нуждаться', 'fi': 'tarvita', 'type': 5},
        {'ru': 'управлять', 'fi': 'hoitaa', 'type': 1},
        {'ru': 'помогать', 'fi': 'auttaa', 'type': 1},
        {'ru': 'запасать', 'fi': 'varata', 'type': 4},
        {'ru': 'заказывать (напитки)', 'fi': 'tilata', 'type': 4},
        {'ru': 'родиться', 'fi': 'syntyä', 'type': 1},
        {'ru': 'жить', 'fi': 'elää', 'type': 1},
        {'ru': 'умереть', 'fi': 'kuolla', 'type': 3},
        {'ru': 'искать', 'fi': 'etsiä', 'type': 1},
        {'ru': 'находить', 'fi': 'löytää', 'type': 1},
        {'ru': 'открыть', 'fi': 'avata', 'type': 4},
        {'ru': 'закрыть', 'fi': 'sulkea', 'type': 1},
        {'ru': 'чинить', 'fi': 'korjata', 'type': 4},
        {'ru': 'хватать (достаточно)', 'fi': 'riittää', 'type': 1},
        {'ru': 'петь', 'fi': 'laulaa', 'type': 1},
        {'ru': 'случаться', 'fi': 'tapahtua', 'type': 1},
        {'ru': 'начинаться', 'fi': 'alkaa', 'type': 1},
        {'ru': 'начинать', 'fi': 'aloittaa', 'type': 1},
        {'ru': 'заканчивать', 'fi': 'loppua', 'type': 1},
    ]

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

    def __init__(self):
        self.correct_verb = None

    def new_choose_one_question(self, options_count=4):
        options = random.sample(self.VERBS, k=options_count)
        self.correct_verb = random.choice(options)
        return {
            'correct_verb': self.correct_verb,
            'options': options
        }

    def new_end_question(self):
        selected_verb = random.choice(self.VERBS)
        selected_pronoun = random.randint(1, 6)
        answer = self.conjure_verb(selected_verb, selected_pronoun)
        self.correct_verb = answer
        return {
            'answer': answer,
            'verb': selected_verb,
            'pronoun': self.PRONOUNS[selected_pronoun]['pronoun']
        }

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
                verb_base = verb[:-1]
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

        if pronoun == 3 or pronoun == 6:
            return verb_base + self.make_end_for_third_person(verb_base)
        return verb_base + self.PRONOUNS[pronoun]['ending']

    def make_end_for_third_person(self, verb_base: str, plural=False) -> str:
        if plural:
            if 'a' in verb_base or 'o' in verb_base or 'u' in verb_base:
                return 'vat'
            return 'vät'
        if verb_base.endswith('aa') or verb_base.endswith('ää'):
            return ''
        return verb_base[-1]

    def check_answer(self, answer: str) -> bool:
        return answer.lower() == self.correct_verb.lower()

    def get_correct_answer(self) -> str:
        return self.correct_verb.lower()

    def new_question_multiple(self, options_count=4):
        options = random.sample(self.VERBS, k=options_count)
        self.correct_verb = random.choice(options)
        return {
            'correct_answer': self.correct_verb,
            'options': options
        }



