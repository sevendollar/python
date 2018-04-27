#!/usr/local/bin/python3

import time

block = '\u2588'
status_bar = block
while True:
    for p in range(101):
        print(f'{p}% >> {status_bar}', '\r', end='')
        if p % 2 == 0:
            status_bar += block
        time.sleep(0.03)
        if p == 100:
            print(f'{p}% >> {status_bar + block}')
    break
print('Done!')
