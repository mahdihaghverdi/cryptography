"""This module contains the pre data that is needed to
encode and decode an affine cipher
"""

from collections import namedtuple
from math import gcd

__all__ = [
    'persian_letters',
    'persian_ctable',
    'persian_dtable',
    'Key',
    'keys',
    'MOD32',
    'PHI32',
    'mul_reverses'
]

# letters table
persian_letters = 'ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'
assert len(persian_letters) == 32

persian_ctable = dict(zip(persian_letters, range(32)))
persian_dtable = dict(zip(range(32), persian_letters))

# (a, b) keys
Key = namedtuple('Key', 'a b')

as_ = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31]
assert len(as_) == 2**5 - 2**4
assert all(gcd(i, 32) == 1 for i in as_)

bs = range(32)
keys = [Key(_a, _b) for _a in as_ for _b in bs]

assert len(keys) == len(as_) * 32

# CONSTANTS
MOD32 = 32
PHI32 = len(as_)


# the reverses of as
def compute_ar(a, phi=PHI32):
    """a_reverse = a^(PHI32-1) % MOD32"""
    return (a ** (phi - 1)) % MOD32


mul_reverses = {a: compute_ar(a) for a in as_}
assert all([(a * ar % MOD32 == 1) for a, ar in mul_reverses.items()])
