from functools import wraps
from inspect import getfullargspec
from itertools import islice
from typing import TypeAlias, Literal

import rich
from rich.table import Table

BitMat: TypeAlias = list[list[int]]


def batched(iterable, n):
    # batched('ABCDEFG', 3) -> ABC DEF G
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def stream_to_matrix(stream: str) -> BitMat:
    """Make the stream a matrix converted as an integers

    Arguments:
        stream: b0b1b2...b15

    Return:
        [[b0, b4, b8, b12],
         [b1, b5, b9, b13],
         [b2, b6, b10, b14],
         [b3, b7, b11, b15]]
    """
    ranges = []
    s = 0
    for i in range(0, 128 // 8):
        e = s + 8
        ranges.append((s, e))
        s = e

    mat = [[], [], [], []]
    for r in batched(ranges, 4):
        for idx, ra in enumerate(r):
            s, e = ra
            _stream = int(stream[s:e], 2)
            mat[idx].append(_stream)
    return mat


def matrix_to_stream(matrix: BitMat) -> str:
    """Make the matrix a stream

    Arguments:
        matrix: [[b0, b4, b8, b12],
                 [b1, b5, b9, b13],
                 [b2, b6, b10, b14],
                 [b3, b7, b11, b15]]

    Return:
        'b0b1b2b3...b15'
    """
    stream = ''
    for col in range(4):
        _stream = ''
        for row in matrix:
            _stream += f'{bin(row[col])[2:]:0>8}'
        stream += _stream
    return stream


def type_and_len_check(func):
    @wraps(func)
    def wrapper(*args):
        argnames = getfullargspec(func).args
        for arg, name in zip(args, argnames):
            if not isinstance(arg, str):
                raise TypeError(f'{name!r} should be `str`')

        for arg, name in zip(args, argnames):
            if not len(arg) == 128:
                raise ValueError(f'{name!r} should 128 bits')

        return func(*args)

    return wrapper


@type_and_len_check
def get_change_ratio(before, after) -> tuple[int, float, str]:
    """Return number of changed bits and ratio of the change"""
    ratio = 0
    difference = ''
    for b, a in zip(before, after):
        is_not = int(b) ^ int(a)
        ratio += is_not
        if is_not:
            difference += '^'
        else:
            difference += ' '
    return ratio, ratio / 128 * 100, difference


def print_operation_table(operation: Literal['sb', 'sr', 'mc', 'ark', 'fr'], count, ratio):
    match operation:
        case 'sb':
            title = 'SB: Sub Bytes'
        case 'sr':
            title = 'SR: Shift Row'
        case 'mc':
            title = 'MC: Mix Column'
        case 'ark':
            title = 'ARK: Add Round Key'
        case 'fr':
            title = 'FR: Full Round'
        case _:
            raise ValueError("Operation must be one of 'sb', 'sr', 'mc' or 'ark'.")

    table = Table("Changed bit No.", 'Bit change ratio', title=title, show_lines=True)
    table.add_row('Cnt', f'[green]{count}[/green]')
    table.add_row('ratio', f'[bold yellow]{ratio}%[/yellow bold]')
    rich.print(table)


def print_ct_ct_diff(ct1, ct2):
    rich.print(f'[white]C1[/white]:[bold blue]{ct1}[/blue bold]')
    rich.print(f'[white]C2[/white]:[bold magenta]{ct2}[/magenta bold]')
    _, __, diff = get_change_ratio(ct1, ct2)
    rich.print(f'[bold red]   [underline]{diff}[/red bold][/underline]')
    print()


def print_pt_ct_diff(pt, ct, num):
    rich.print(f'[white]P{num}[/white]:[bold blue]{pt}[/blue bold]')
    rich.print(f'[white]C{num}[/white]:[bold magenta]{ct}[/magenta bold]')
    _, __, diff = get_change_ratio(pt, ct)
    rich.print(f'[bold red]   [underline]{diff}[/red bold][/underline]')
    print()
