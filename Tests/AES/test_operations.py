from AES.operations import _stream_to_matrix, _matrix_to_stream, sub_bytes, isub_bytes, shift_row

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


numbers = [
    [0x01, 0x02, 0x03, 0x84],
    [0x04, 0x05, 0x16, 0xba],
    [0x17, 0x18, 0x19, 0xec],
    [0x1d, 0x1e, 0x1f, 0xf7]
]

answers = [
    [0x7c, 0x77, 0x7b, 0x5f],
    [0xf2, 0x6b, 0x47, 0xf4],
    [0xf0, 0xad, 0xd4, 0xce],
    [0xa4, 0x72, 0xc0, 0x68]
]


def test_sub_bytes():
    assert sub_bytes(_matrix_to_stream(numbers)) == _matrix_to_stream(answers)


def test_isub_bytes():
    assert isub_bytes(_matrix_to_stream(answers)) == _matrix_to_stream(numbers)


shifted = [
    [0, 4, 8, 12],
    [5, 9, 13, 1],
    [10, 14, 2, 6],
    [15, 3, 7, 11],
]


def test_shift_rows():
    assert shift_row(_matrix_to_stream(mat)) == _matrix_to_stream(shifted)
