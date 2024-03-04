"""This module contains the encode and decode functions of affine cipher"""
from affine_break import Key, persian_ctable, MOD32, mul_reverses, persian_dtable, keys, persian_letters


def encode(pt: str, key: Key) -> str:
    """Ci = aPi + b % MOD"""
    return persian_dtable[(key.a * persian_ctable[pt] + key.b) % MOD32]


def decode(ct: str, key: Key) -> str:
    """Pi = (Ci - b) / a % MOD === (Ci - b) * a_reverse % MOD"""
    return persian_dtable[((persian_ctable[ct] - key.b) * mul_reverses[key.a]) % MOD32]


key_ = keys[6]
assert all([pt == decode(encode(pt, key_), key_) for pt in persian_letters])
