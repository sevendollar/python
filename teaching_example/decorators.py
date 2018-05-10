import re
import functools


def make_args_to_go_upper(func, *ARGS, **KWARGS):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        origin_func = func(*args, **kwargs)
        pattern = r'\((.*)\).*\{.*\}'
        match = re.finditer(pattern, origin_func)
        new_func = ''.join(_.group() for _ in match).upper() or None
        return new_func or origin_func
    return wrapper


def bark(origin_func):
    @functools.wraps(origin_func)
    def wrapper(*args, **kwargs):
        return f'<bark>{origin_func(*args, **kwargs)}</bark>'
    return wrapper


def whisper(origin_func):
    @functools.wraps(origin_func)
    def wrapper(*args, **kwargs):
        return f'<whisper>{origin_func(*args, **kwargs)}</whisper>'
    return wrapper


@bark
@whisper
@make_args_to_go_upper
def greeting(*args, **kwargs):
    # return f'hello world!'
    return f'{args}, {kwargs}'


# print(greeting.__name__)
# print(make_args_to_go_upper.__name__)
print(greeting('jef', 'lves', 'python', name='jef', skill='python'))