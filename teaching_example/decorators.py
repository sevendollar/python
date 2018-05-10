import re
import functools


def make_args_to_go_upper(func, *ARGS, **KWARGS):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        origin_func = func(*args, **kwargs)
        pattern = r'\((.*)\).*\{.*\}'
        match = re.finditer(pattern, origin_func)
        new_func = ''.join(_.group() for _ in match).upper() or None
        return new_func
    return wrapper


@make_args_to_go_upper
def greeting(*args, **kwargs):
    # return f'args: {args}, {kwargs}'
    return f'{args}, {kwargs}'


# print(greeting.__name__)
# print(make_args_to_go_upper.__name__)
print(greeting('jef', 'lves', 'python', name='jef', skill='python'))