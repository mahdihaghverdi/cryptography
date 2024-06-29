# Shamir Secret Sharing Schema
import random


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

    template = '{co}x^{po}'
    coefficients = [
        template.format(co=f[c], po=p)
        for c, p in zip(range(t), reversed(range(t)))
    ]
    print(f'f(x) = {" + ".join(coefficients)}')

    return {i: f.calculate(i) % p for i in range(1, n + 1)}
