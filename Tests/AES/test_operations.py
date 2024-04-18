import pytest

from AES.operations import _stream_to_matrix, _matrix_to_stream

strm = ''
for num in range(16):
    strm += f'{bin(num)[2:]:0>8}'

mat = [
    [0, 4, 8, 12],
    [1, 5, 9, 13],
    [2, 6, 10, 14],
    [3, 7, 11, 15],
]


def test_stream_to_matrix():
    assert _stream_to_matrix(strm) == mat


def test_matrix_to_stream():
    assert strm == _matrix_to_stream(mat)
