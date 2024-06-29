# Shamir Secret Sharing Schema


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
