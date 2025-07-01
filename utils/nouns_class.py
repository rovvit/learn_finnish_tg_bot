from xmlrpc.server import resolve_dotted_attribute

from utils.KPT_transform import KPT_transform, VOWELS, HARD_VOWELS

CASES = {
        1: {'name': 'Genetiivi', 'isKPT': True, 'q_pers': 'Kenen', 'q_nonpers': 'Minkä'},
        2: {'name': 'Partitiivi', 'isKPT': False, 'q_pers': 'Ketä', 'q_nonpers': 'Mitä'},
        3: {'name': 'Illatiivi', 'isKPT': False, 'q_pers': None, 'q_nonpers': 'Mihin'},
        4: {'name': 'Allatiivi', 'isKPT': True, 'q_pers': None, 'q_nonpers': 'Mihin'},
    }

class NounWord:
    def __init__(self, data):
        self.fi = data['fi']
        self.ru = data['ru']
        if data['base']:
            self.base = data['base']
        self.isFinnish = data['isFinnish']

    def inflict(self, case: int) -> str:
        match case:
            case 1:
                return self.inflict_genetiivi()
            case 2:
                return self.inflict_partitiivi()

            case _:
                raise Exception('No such case!')

    def inflict_genetiivi(self) -> str:
        # word = self.fi
        # word_KPTed = KPT_transform(self.fi)
        # if word[-1] in VOWELS:
        #     if word_KPTed[-1:] == 'e':
        #         return word_KPTed + 'en'
        #     if word[-1:] == 'i':
        #         if self.isFinnish:
        #             if word_KPTed[-2:] == 'si':
        #                 return word_KPTed[:-2] + 'den'
        #             return word_KPTed[:-1] + 'en'
        #     return word_KPTed + 'n'
        # elif word[-3:] == 'nen':
        #     return word_KPTed[:-3] + 'sen'
        # elif word[-2:] in ['as', 'äs']:
        #     return word_KPTed[:-1] + word_KPTed[-2] + 'n'
        # elif word[-2:] == 'is':
        #     # тут должен быть if потому что iksen
        #     return word_KPTed[:-1] + 'in'
        # elif word[-2:] in ['us', 'ys']:
        #     # тут должен быть if потому что iksen
        #     return word_KPTed[:-1]  + 'den'
        # elif word[-2:] in ['os', 'ös']:
        #     return word_KPTed[:-1]  + 'ksen'
        # elif word[-3:] in ['ton', 'tön']:
        #     if word_KPTed[-2] == 'ö':
        #         return word_KPTed[:-3] + 'ttömän'
        #     return word_KPTed[:-3]  + 'ttoman'
        # elif word_KPTed[-2:] == 'in':
        # тут надо починить КРТ
        #     return word_KPTed[:-2] + 'imen'
        # elif word_KPTed[-2:] == 'ut':
        #     pass
        # elif word_KPTed[-3] in ['tar', 'tär']:
        #     pass
        # elif not self.isFinnish:
        #     return self.fi + 'in'
        # else:
        #     raise Exception("I don't know how to inflict that :(")
        return str(self.base) + 'n'

    def inflict_partitiivi(self) -> str:
        word = self.fi
        if word[-1] in VOWELS and word[-2] not in VOWELS:
            if word[-1] == 'i' and self.isFinnish:
                result = word[:-1] + 'e'
            elif word[-1] == 'e':
                result = word + 'tt'
            else:
                result = word
        else:
            if word[-3:] == 'nen':
                result = word[:-3] + 'st'
            else:
                result = word + 't'
        if any(letter in word for letter in HARD_VOWELS):
            return result + 'a'
        else:
            return result + 'ä'


if __name__ == '__main__':
    word = {'fi': 'puhelin', 'ru': '', 'isFinnish': True }
    print(NounWord(word).inflict_genetiivi())