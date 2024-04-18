"""This module contains the encode and decode functions of affine cipher"""
from Affine import Key, persian_ctable, MOD32, mul_reverses, persian_dtable, keys, persian_letters


def _encode(pt: str, key: Key) -> str:
    """Ci = aPi + b % MOD"""
    return persian_dtable[(key.a * persian_ctable[pt] + key.b) % MOD32]


def _decode(ct: str, key: Key) -> str:
    """Pi = (Ci - b) / a % MOD === (Ci - b) * a_reverse % MOD"""
    return persian_dtable[((persian_ctable[ct] - key.b) * mul_reverses[key.a]) % MOD32]


key_ = keys[6]
assert all([pt == _decode(_encode(pt, key_), key_) for pt in persian_letters])


def encrypt(pt: str, key: Key) -> str:
    """Encrypt the plain text"""
    return ''.join(_encode(char, key) for char in pt)


def decrypt(ct: str, key: Key) -> str:
    """Decrypt the cipher text"""
    return ''.join(_decode(char, key) for char in ct)
