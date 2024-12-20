# Shamir Secret Sharing Schema
import math
import random


def calculate_reverse(n, p):
    phi = sum(1 for num in range(1, p) if math.gcd(num, p) == 1)
    return (n ** (phi - 1)) % p


class F:
    def __init__(self):
        self.coefficients = []

    def __getitem__(self, item):
        return self.coefficients[item]

    def add_co(self, co):
        self.coefficients.append(co)

    def calculate(self, n):
        # f(x) = 3x^2 + -1x + 8
        return sum(
            co * (n ** power)
            for power, co in enumerate(reversed(self.coefficients))
        )

    def print(self, t):
        template = '{co}x^{po}'
        coefficients = [
            template.format(co=self[c], po=p)
            for c, p in zip(range(t), reversed(range(t)))
        ]
        print(f'f(x) = {" + ".join(coefficients)}')


def deal(s: int, n: int, t: int, p: int) -> dict[int: int]:
    """Calculate the shares

    :param s: The secret (``s %= p``)
    :param n: Number of shares
    :param t: Number of required parties to share their value
    :param p: The modulos (must be prime)
    :return: A dictionary of ``{x: f(x)%p}``
    """
    if t > n:
        raise ValueError(f"t must be lesser than or equal to n")

    f = F()
    for _ in range(t - 1):
        f.add_co(random.randint(1, p - 1))
    f.add_co(s % p)
    f.print(t)

    return {i: f.calculate(i) % p for i in range(1, n + 1)}


def secret(t: int, p: int, y: dict[int, int]) -> int:
    """

    :param t: Number of parties to share their value
    :param p: The modulos
    :param y: A dictionary of ``{x: f(x) % p}``
    :return: The secret
    """
    if len(y) < t:
        raise ValueError("Number of shares should be greater than or equal to t")

    sec = 0
    for i in y:
        yi = y[i]
        prod = 1
        for j in y:
            if j != i:
                prod *= (j * calculate_reverse(j - i, p))
        sec += yi * prod
    return sec % p


deals = deal(4, 10, 3, 13)
print(deals)
print(secret(3, 13, {3: deals[3], 5: deals[5], 7: deals[7], 8: deals[8]}))
