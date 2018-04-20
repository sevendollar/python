#!/bin/sh/python

import re

text = '''
'''

REGEX_ITEMS = ['macs', 'customer_id', 'chinese_characters', 'bad_words']
REGEX_PATTERNS = [r'([\w\d]+[:-]){5}[\w\d]+', r'[a-z][0-9]{9}', r'[\u4e00-\u9fff]+', r'(fuck|shit|fxxk|fxk|ass)']


def is_mac_legal(mac):
    mac_regex = re.compile(r'([a-f0-9]{2}[:-]){5}[a-f0-9]{2}', re.IGNORECASE)
    return mac_regex.match(mac) and True or False


def __regex_match(pattern, text_, regex):
    return {regex: tuple(x.group() for x in re.finditer(pattern, text_, re.IGNORECASE)) or None}


def result(pattern, text_, regex):
    text_ = [text_] * len(regex)
    r = {}
    for m in map(__regex_match, pattern, text_, regex):
        r = {**r, **m}

    if len(r.get('chinese_characters') or '') == 3:
        r['team_name'] = r.get('chinese_characters')[0]
        r['team_user'] = r.get('chinese_characters')[1]
        r['customer_name'] = r.get('chinese_characters')[2]

    for mac in r.pop('macs') or '':  # check mac legality.
        if is_mac_legal(mac):
            # when is legal, put it back in the dict.
            r['macs'] = r.get('macs', tuple()) + (mac.lower(),)
        else:
            # when illegal, put it in the dict and name it "fake_mac".
            r['fake_macs'] = r.get('fake_macs', tuple()) + (mac.lower(),)
    return r


def is_data_legal(result):
    return (
        (not result.get('fake_macs'))
        and
        result.get('macs')
        and
        (len(result.get('chinese_characters')) == 3)
        and
        result.get('customer_id')
    ) and True or False


def is_data_legal_v2(result):
    check_point = ()
    if len(result.get('chinese_characters') or '') != 3:
        check_point += 'name',
    if not result.get('customer_id'):
        check_point += 'id',
    if not result.get('macs'):
        check_point += 'mac',
    if result.get('fake_macs'):
        check_point += result.get('fake_macs')
    return (not check_point) and (True, None) or (False, check_point)
    # return check_point or True


if __name__ == '__main__':
    rs = result(REGEX_PATTERNS, text, REGEX_ITEMS)
    print(f'User inputs: {rs}')
    print(f'Is inputs right? {is_data_legal_v2(rs)}')


