# practice of map example

import re

text = '''
'''

# regular uses
MAC_REGEX = r'([\w\d]+[:-]){5}[\w\d]+'
ID_REGEX = r'[a-zA-Z][0-9]{9}'
CHINESE_CHARACTER_REGEX = r'[\u4e00-\u9fff]+'
BAD_WORDS_REGEX = f'(fuck|shit|fxxk|fxk|ass)'

mac_matches = re.finditer(MAC_REGEX, text, re.IGNORECASE)
id_matches = re.finditer(ID_REGEX, text)
chinese_matches = re.finditer(CHINESE_CHARACTER_REGEX, text)
bad_words_matches = re.finditer(BAD_WORDS_REGEX, text, re.IGNORECASE)
chinese_characters = tuple(c[0] for c in chinese_matches)

result = {
    'mac': tuple(m.group() for m in mac_matches) or None,
    'chinese': chinese_characters or None,
    'id': tuple(i.group() for i in id_matches) or None,
    'bad_words': tuple(b.group() for b in bad_words_matches) or None
}
print(result)



# cool uses
regex = ['mac', 'id', 'chinese', 'bad_word']
pattern = ['([a-f0-9]{2}[:-]){5}[a-f0-9]{2}', '[a-z][0-9]{9}', '[\\u4e00-\\u9fff]+', f'(fuck|shit|fxxk|fxk|ass)']

def regex_match(pattern, text, regex):
    return {regex: tuple(x.group() for x in re.finditer(pattern, text, re.IGNORECASE)) or None}

def regex_matches(pattern, text, regex):
    result = {}
    for m in map(regex_match, pattern, text, regex):
        result = {**result, **m}
    return result

print(regex_matches(pattern, [text] * len(regex), regex))
