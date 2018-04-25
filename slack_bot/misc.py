#!/bin/sh/python

import re
import json

REGEXs = {
    'macs': r'([a-z0-9]+[:-]){5}[a-z0-9]{0,2}',
    # 'macs': r'([\w\d]+[:-]){5}[\w\d]+',
    'customer_id': r'[a-z][0-9]{9}',
    'chinese_characters': r'[\u4e00-\u9fff]+',
    'bad_words': r'(fuck|shit|fxxk|fxk|ass)'
}

REGEX_ITEMS = [x for x in REGEXs.keys()]
REGEX_PATTERNS = [y for y in REGEXs.values()]

# REGEX_ITEMS = ['macs', 'customer_id', 'chinese_characters', 'bad_words']
# REGEX_PATTERNS = [r'([\w\d]+[:-]){5}[\w\d]+', r'[a-z][0-9]{9}', r'[\u4e00-\u9fff]+', r'(fuck|shit|fxxk|fxk|ass)']


#  TODO: check if id is legal.
def is_id_legal(id):
    pass


def is_mac_legal(mac):
    mac_regex = re.compile(r'([a-f0-9]{2}[:-]){5}[a-f0-9]{2}', re.IGNORECASE)
    return mac_regex.match(mac) and True or False


def __regex_match(regex, pattern, text_):
    text_ = text_ or ''  # if value is None covert to '' so that re.finditer won't go wrong.
    return {regex: tuple(x.group() for x in re.finditer(pattern, text_, re.IGNORECASE)) or None}


def parser(text_=None, regex=REGEX_ITEMS, pattern=REGEX_PATTERNS):
    text_ = [
               {
                   tuple: lambda x: ' '.join(str(i) for i in x),
                   set: lambda x: ' '.join(str(i) for i in x),
                   list: lambda x: ' '.join(str(i) for i in x),
                   dict: lambda x: json.dumps(x),
                   str: lambda x: x
               }.get(type(text_), lambda x: str(text_))(text_)
           ] * len(regex)
    # text_ = type(text_) in (tuple, list, set) and ' '.join(text_) or text_  # covert from tuple or list or set to str
    # text_ = type(text_) is dict and json.dumps(text_) or text_  # covert from dict to str
    # text_ = [text_] * len(regex)
    result = {}

    for m in map(__regex_match, regex, pattern, text_):
        result = {**result, **m}

    if len(result.get('chinese_characters') or '') == 3:
        result['team_name'] = result.get('chinese_characters')[0]
        result['team_user'] = result.get('chinese_characters')[1]
        result['customer_name'] = result.get('chinese_characters')[2]

    for mac in result.pop('macs') or '':  # check mac legality.
        if is_mac_legal(mac):
            # when is legal, put it back in the dict.
            result['macs'] = result.get('macs', tuple()) + (mac.lower(),)
        else:
            # when illegal, put it in the dict and name it "fake_mac".
            result['fake_macs'] = result.get('fake_macs', tuple()) + (mac.lower(),)

    # deduplicat macs
    result['macs'] = deduplicate(result.get('macs'))
    result['fake_macs'] = deduplicate(result.get('fake_macs'))

    return result


def deduplicate(x):
    r = []
    for i in x:
        if i not in r:
            r.append(i)
    return tuple(r)


# def is_data_legal(result):
#     return (
#         (not result.get('fake_macs'))
#         and
#         result.get('macs')
#         and
#         (len(result.get('chinese_characters')) == 3)
#         and
#         result.get('customer_id')
#     ) and True or False


def is_add_mac_legal(result):
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
    pass


