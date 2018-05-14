x = 3
y = -3


# regular use
def judgement(x, y):
    if x > y:
        return 'x'
    elif x < y:
        return 'y'
    else:
        return 'equal'

answer = judgement(x, y)
print(f'answer: {answer}')


# cool use
answer2 = (lambda x, y: 'x' if x > y else ('y' if x < y else 'equal'))(x, y)
print(f'answer2: {answer2}')


# You can use a ternary expression in Python, but only for expressions, not for statements.
def is_great_than(x, y):
    if x > y:
        return True
    else:
        False

def is_equal(x, y):
    if x == y:
        return True
    else:
        False

answer3 = 'x' if is_great_than(x, y) else ('equal' if is_equal(x, y) else 'y')
print(f'answer3: {answer3}')
