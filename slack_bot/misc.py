#!/bin/sh/python

import re


def is_id_legal(id):
    #  TODO: check if id is legal.
    pass


def is_mac_legal(mac):
    mac_regex = re.compile('([a-f0-9]{2}[:-]){5}[a-f0-9]{2}', re.IGNORECASE)
    return mac_regex.match(mac) and True or False


def parsed_data(words):
    # MAC_REGEX = r'([a-zA-Z0-9]{2}[:-]){5}[a-zA-Z0-9]{2}'
    MAC_REGEX = r'([\w\d]+[:-]){5}[\w\d]+'
    ID_REGEX = r'[a-zA-Z][0-9]{9}'
    CHINESE_CHARACTER_REGEX = r'[\u4e00-\u9fff]+'
    BAD_WORDS_REGEX = f'(fuck|shit|fxxk|fxk|ass)'

    mac_matches = re.finditer(MAC_REGEX, words, re.IGNORECASE)
    id_matches = re.finditer(ID_REGEX, words)
    chinese_matches = re.finditer(CHINESE_CHARACTER_REGEX, words)
    bad_words_matches = re.finditer(BAD_WORDS_REGEX, words, re.IGNORECASE)
    chinese_characters = tuple(c[0] for c in chinese_matches)

    if len(chinese_characters) == 3:
        team_name, team_user, customer_name = chinese_characters[0], chinese_characters[1], chinese_characters[2]
    else:
        team_name, team_user, customer_name = None, None, None

    new_words = {
        'macs': tuple(m.group() for m in mac_matches) or None,
        'chinese_characters': chinese_characters or None,
        'team_name': team_name,
        'team_user': team_user,
        'customer_name': customer_name,
        'customer_id': tuple(i.group() for i in id_matches) or None,
        'bad_words': tuple(b.group() for b in bad_words_matches) or None
    }
    return new_words


def wrong_data(data):
    check_point = ()
    if not (data.get('team_name', None) and data.get('team_user', None and data.get('customer_name', None))):
        check_point += 'name',
    if not data.get('customer_id', None):
        check_point += 'id',
    if data.get('bad_words', None):
        check_point += 'language',
    if data.get('macs', None):
        for mac in data.get('macs', None):
            if not is_mac_legal(mac):
                check_point += mac,
    else:
        check_point += 'macs',

    return check_point or False


text_ = '''
'''

if __name__ == '__main__':
    if wrong_data(parsed_data(text_)) is False:
        print('data ok')
    else:
        print('wrong data', str(wrong_data(parsed_data(text_))))
