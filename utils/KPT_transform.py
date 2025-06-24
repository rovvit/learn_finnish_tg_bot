PAIRS = {
    'kk': 'k',
    'pp': 'p',
    'tt': 't',

    'k': '',
    'p': 'v',
    't': 'd',

    'rt': 'rr',
    'lt': 'll',
    'nt': 'nn',
    'nk': 'ng',
    'np': 'mm'
}

VOWELS = [ 'a', 'o', 'u', 'e', 'i', 'ä', 'ö', 'y' ]
HARD_VOWELS = [ 'a', 'o', 'u' ]


def KPT_transform(word_base: str, is_forward: bool = True):
    ending = word_base[-3:]
    if ending[2] in VOWELS:
        ending = ending[:2]
    if is_forward:
        if ending in PAIRS:
            return word_base[:-3] + word_base[-3:].replace(ending, PAIRS[ending])
        else:
            ending = ending[-1:]
            if ending in PAIRS:
                return word_base[:-2] + word_base[-2:].replace(ending, PAIRS[ending])
        return word_base
    else:
        pass
