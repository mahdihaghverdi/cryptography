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

result = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]


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
    _r = result.copy()

    for col in range(4):
        for row in range(4):
            sb = _sub_byte(input_stream[row][col])
            _r[row][col] = sb
    return _r


def _isub_bytes(input_stream: BitMat) -> BitMat:
    _r = result.copy()

    for col in range(4):
        for row in range(4):
            sb = _isub_byte(input_stream[row][col])
            _r[row][col] = sb
    return _r


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


############ SR: Shift Rows ############  # noqa: E266
def _rotate_left(row: list, rotate: int):
    for _ in range(rotate):
        got = row.pop(0)
        row.append(got)


def _shift_rows(input_stream: BitMat) -> BitMat:
    _input_stream = input_stream.copy()
    for idx, row in enumerate(_input_stream):
        _rotate_left(row, idx)

    return _input_stream


def shift_row(stream: str) -> str:
    """ShiftRow the stream

    Arguments:
        stream: b1b2b3...b15

    Returns:
        stream of:
            [[b0, b4, b8, b12],
             [b5, b9, b13, b1],
             [b10, b14, b2, b6],
             [b15, b3, b7, b11]]
    """
    strm = _stream_to_matrix(stream)
    return _matrix_to_stream(_shift_rows(strm))


############ MC: Mix Columns ############  # noqa: E266
mc_mat = GF128(
    [[0x02, 0x03, 0x01, 0x01],
     [0x01, 0x02, 0x03, 0x01],
     [0x01, 0x01, 0x02, 0x03],
     [0x03, 0x01, 0x01, 0x02]]
)


def _mix_columns(input_stream: BitMat) -> BitMat:
    _r = []
    got = GF128(input_stream)
    _result = got @ mc_mat
    for row in _result:
        _r.append([num for num in row])
    return _r


def mix_columns(stream: str) -> str:
    """MixColumn the stream

    Arguments:
        stream: b1b2b3...b4

    Return:
        apply a matrix multiplication and return the stream
        c1c2c3...c15
    """
    _is = _stream_to_matrix(stream)
    return _matrix_to_stream(_mix_columns(_is))


print(GF128(0x01) * GF128(0x02))
