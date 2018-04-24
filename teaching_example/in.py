# ragular uses
a = 0
b = 1
if a == 0 or b == 0:
    print('found 0s.')

# cool uses
if 0 in (a, b):
    print('found 0s.')



# ragular uses
a = [12, 33, 0, 105, 8]
for i in a:
    if i == 0:
        print('found 0s')

# cool uses
a = [12, 33, 0, 105, 8]
if 0 in a:
    print('found 0s')
