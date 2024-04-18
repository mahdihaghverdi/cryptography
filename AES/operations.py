"""This module implements 4 operations present in AES
- SB: Sub Bytes
- SR: Shift Rows
- MC: Mix Columns
- ARK: Add Round Key
"""
from itertools import islice
from typing import TypeAlias

import galois

BitMat: TypeAlias = list[list[int]]

GF128 = galois.GF(2, 8, irreducible_poly='x^8 + x^4 + x^3 + x + 1')


def batched(iterable, n):
    # batched('ABCDEFG', 3) -> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def _stream_to_matrix(stream: str) -> BitMat:
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


def _matrix_to_stream(matrix: BitMat) -> str:
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


############ SB: Sub Bytes ############  # noqa: E266
sb_mat = GF128(
    [[1, 0, 0, 0, 1, 1, 1, 1],
     [1, 1, 0, 0, 0, 1, 1, 1],
     [1, 1, 1, 0, 0, 0, 1, 1],
     [1, 1, 1, 1, 0, 0, 0, 1],
     [1, 1, 1, 1, 1, 0, 0, 0],
     [0, 1, 1, 1, 1, 1, 0, 0],
     [0, 0, 1, 1, 1, 1, 1, 0],
     [0, 0, 0, 1, 1, 1, 1, 1]],
)

isb_mat = GF128(
    [[0, 0, 1, 0, 0, 1, 0, 1],
     [1, 0, 0, 1, 0, 0, 1, 0],
     [0, 1, 0, 0, 1, 0, 0, 1],
     [1, 0, 1, 0, 0, 1, 0, 0],
     [0, 1, 0, 1, 0, 0, 1, 0],
     [0, 0, 1, 0, 1, 0, 0, 1],
     [1, 0, 0, 1, 0, 1, 0, 0],
     [0, 1, 0, 0, 1, 0, 1, 0]],
)

b = GF128([[1], [1], [0], [0], [0], [1], [1], [0]])
ib = GF128([[1], [0], [1], [0], [0], [0], [0], [0]])


def _sub_byte(byte: int) -> int:
    """SubByte the integer according to s(x) = ax^(-1)+b"""
    number = GF128(byte)
    rev = GF128(number) ** -1 if byte != 0 else 0
    mat = GF128([[char] for char in reversed(f'{bin(rev)[2:]:0>8}')])
    result = (sb_mat @ mat) + b
    num = ''
    for bit in reversed(result):
        num += str(bit[0])
    return int(num, 2)


def _isub_byte(byte: int) -> int:
    number = GF128(byte)
    mat = GF128([[char] for char in reversed(f'{bin(number)[2:]:0>8}')])
    result = (isb_mat @ mat) + ib
    num = ''
    for bit in reversed(result):
        num += str(bit[0])
    rev = int(num, 2)
    res = GF128(rev) ** -1 if byte != 0 else 0
    return res


def _sub_bytes(input_stream: BitMat) -> BitMat:
    result = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    for col in range(4):
        for row in range(4):
            sb = _sub_byte(input_stream[row][col])
            result[row][col] = sb
    return result


def _isub_bytes(input_stream: BitMat) -> BitMat:
    result = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    for col in range(4):
        for row in range(4):
            sb = _isub_byte(input_stream[row][col])
            result[row][col] = sb
    return result


def sub_bytes(stream: str) -> str:
    """Sub byte the stream

    Arguments:
        stream: b1b2b3...b15

    Return: s1s2s3...s15
    """
    _is = _stream_to_matrix(stream)
    return _matrix_to_stream(_sub_bytes(_is))


def isub_bytes(stream: str) -> str:
    """Inverse sub byte the stream

    Arguments:
        stream: s1s2s3...s15

    Return: b1b2b3...b15
    """
    _is = _stream_to_matrix(stream)
    return _matrix_to_stream(_isub_bytes(_is))
