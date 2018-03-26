#!/bin/python

import datetime

def star_sign(date):
    year, month, day = str(date).split('-')
    year = int(year)
    month = int(month)
    day = int(day)
    birthday = datetime.date(year, month, day)

    if datetime.date(year, 3, 21) <= birthday <= datetime.date(year, 4, 19):
        return 'aries'
    elif datetime.date(year, 4, 20) <= birthday <= datetime.date(year, 5, 20):
        return 'taurus'
    elif datetime.date(year, 5, 21) <= birthday <= datetime.date(year, 6, 20):
        return 'gemini'
    elif datetime.date(year, 6, 21) <= birthday <= datetime.date(year, 7, 22):
        return 'cancer'
    elif datetime.date(year, 7, 23) <= birthday <= datetime.date(year, 8, 22):
        return 'leo'
    elif datetime.date(year, 8, 23) <= birthday <= datetime.date(year, 9, 22):
        return 'virgo'
    elif datetime.date(year, 9, 23) <= birthday <= datetime.date(year, 10, 22):
        return 'libra'
    elif datetime.date(year, 10, 23) <= birthday <= datetime.date(year, 11, 21):
        return 'scorpio'
    elif datetime.date(year, 11, 22) <= birthday <= datetime.date(year, 12, 21):
        return 'sagittatius'
    elif datetime.date(year, 12, 22) <= birthday or birthday <= datetime.date(year, 1, 19):
        return 'capricorn'
    elif datetime.date(year, 1, 20) <= birthday <= datetime.date(year, 2, 18):
        return 'aquarius'
    elif datetime.date(year, 2, 19) <= birthday <= datetime.date(year, 3, 20):
        return 'pisces'
    else:
        return None


def star_sign_range(start, end):
    star_signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittatius', 'capricorn', 'aquarius', 'pisces']
    start_index = star_signs.index(start)
    end_index = star_signs.index(end)

    if (start_index - end_index) <= 0:
        return tuple(i.capitalize() for i in star_signs[start_index:end_index + 1])
    else:
        return tuple(i.capitalize() for i in star_signs[start_index:] + star_signs[:end_index + 1])


MIN_PREGNANCY = 37
MAX_PREGNANCY = 42
today = datetime.date.today()
input_year, input_month, input_day = input('pregnant day(yyyy/mm/dd)?\n').split('/')
pregnant_day = datetime.date(year=int(input_year), month=int(input_month), day=int(input_day))
min_pregnancy_period = datetime.timedelta(weeks=MIN_PREGNANCY)
max_pregnancy_period = datetime.timedelta(weeks=MAX_PREGNANCY)
min_deliver_day = pregnant_day + min_pregnancy_period
max_deliver_day = pregnant_day + max_pregnancy_period

starsign_range = star_sign_range(star_sign(min_deliver_day), star_sign(max_deliver_day))
if min_deliver_day < today or max_deliver_day < today:
    print(f'''you have delivered a bady either with a star sign of '{starsign_range}'... aged {today.year - pregnant_day.year - 1}''')
else:
    min_time_to_deliver, max_time_to_deliver= max_deliver_day - today, min_deliver_day - today
    print(f'''{max_time_to_deliver.days}~{min_time_to_deliver.days} days...deliver day could be between {min_deliver_day} and {max_deliver_day}, will be {starsign_range}''')

