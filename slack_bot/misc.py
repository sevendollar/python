import re


def parse_user_words_v2(words):
    MAC_REGEX = r'([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}'
    ID_REGEX = r'[a-zA-Z][0-9]{9}'
    CHINESE_CHARACTER_REGEX = r'[\u4e00-\u9fff]+'
    BAD_WORDS_REGEX = f'(fuck|shit|fxxk|fxk)'

    mac_matches = re.finditer(MAC_REGEX, words)
    id_matches = re.finditer(ID_REGEX, words)
    chinese_matches = re.finditer(CHINESE_CHARACTER_REGEX, words)
    bad_words_matches = re.finditer(BAD_WORDS_REGEX, words, re.IGNORECASE)

    macs = tuple(m[0] for m in mac_matches)
    ids_ = tuple(i[0] for i in id_matches)
    chinese_characters = tuple(c[0] for c in chinese_matches)
    bad_words = tuple(b[0] for b in bad_words_matches)

    return {'macs': macs, 'ids': ids_, 'chinese_characters': chinese_characters, 'bad_words': bad_words}
