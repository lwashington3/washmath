from abc import abstractmethod
from numpy import sqrt, cbrt
from ..classes import Fraction, Trig, SIN, COS, TAN, CSC, SEC


class Polynomial(object):
    # Key is the power
    def __init__(self, factor_dict:dict, **kwargs):
        self._dict = factor_dict
        try:
            self._variable = kwargs["variable"]
        except KeyError:
            self._variable = "x"

    def __add__(self, other):
        if isinstance(other, float) and isinstance(other, int):
            new_dict = self._dict.copy()
            try:
                new_dict[0] = new_dict[0] + other
            except KeyError:
                new_dict[0] = other
            return Polynomial(new_dict, variable=self._variable)

        elif isinstance(other, Polynomial):
            new_dict = self._dict.copy()
            for other_power, other_coefficient in other._dict.items():
                try:
                    new_dict[other_power] = new_dict[other_power] + other_coefficient
                except KeyError:
                    new_dict[other_power] = other_coefficient
            return Polynomial(new_dict, variable=self._variable)

    def __iadd__(self, other):
        if isinstance(other, float) and isinstance(other, int):
            try:
                self._dict[0] = self._dict[0] + other
            except KeyError:
                self._dict[0] = other

        elif isinstance(other, Polynomial):
            for other_power, other_coefficient in other._dict.items():
                try:
                    self._dict[other_power] += other_coefficient
                except KeyError:
                    self._dict[other_power] = other_coefficient

    def __sub__(self, other):
        if isinstance(other, float) and isinstance(other, int):
            new_dict = self._dict.copy()
            try:
                new_dict[0] = new_dict[0] - other
            except KeyError:
                new_dict[0] = -other
            return Polynomial(new_dict, variable=self._variable)

        elif isinstance(other, Polynomial):
            new_dict = self._dict.copy()
            for other_power, other_coefficient in other._dict.items():
                try:
                    new_dict[other_power] -= other_coefficient
                except KeyError:
                    new_dict[other_power] = -other_coefficient
            return Polynomial(new_dict, variable=self._variable)

    def __isub__(self, other):
        if isinstance(other, float) and isinstance(other, int):
            try:
                self._dict[0] = self._dict[0] - other
            except KeyError:
                self._dict[0] = -other
        elif isinstance(other, Polynomial):
            for other_power, other_coefficient in other._dict.items():
                try:
                    self._dict[other_power] -= other_coefficient
                except KeyError:
                    self._dict[other_power] = -other_coefficient

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            new_dict = {}
            for power, coefficient in self._dict.items():
                new_dict[power] = coefficient * other
            return Polynomial(new_dict, variable=self._variable)
        elif isinstance(other, Polynomial):
            new_dict = {}

            for this_power, this_coefficient in self._dict.items():
                for other_power, other_coefficient in other._dict.items():
                    combined_power = this_power + other_power
                    combined_coefficient = this_coefficient * other_coefficient
                    try:
                        new_dict[combined_power] = new_dict[combined_power] + combined_coefficient
                    except KeyError:
                        new_dict[combined_power] = combined_coefficient

            return Polynomial(new_dict, variable=self._variable)

    def __imul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            for power, coefficient in self._dict.items():
                self._dict[power] = coefficient * other
        elif isinstance(other, Polynomial):
            new_dict = {}

            for this_power, this_coefficient in self._dict.items():
                for other_power, other_coefficient in other._dict.items():
                    combined_power = this_power + other_power
                    combined_coefficient = this_coefficient * other_coefficient
                    try:
                        new_dict[combined_power] = new_dict[combined_power] + combined_coefficient
                    except KeyError:
                        new_dict[combined_power] = combined_coefficient

            self._dict = new_dict

    def __pow__(self, power):
        if isinstance(power, int):
            poly = self.copy()
            for i in range(1, power):
                poly *= self
            return poly
        raise ArithmeticError("Cannot raise powers to decimal numbers at this time")

    def __ipow__(self, power):
        if isinstance(power, int):
            original = self.copy()
            for i in range(1, power):
                self *= original
        else:
            raise ArithmeticError("Cannot raise powers to decimal numbers at this time")

    def __repr__(self) -> str:
        string = ""
        sorted_list = sorted(self._dict.keys())
        sorted_list.reverse()
        for power in sorted_list:
            coefficient = self._dict[power]
            if coefficient != 0:
                string += f" {'+ ' if coefficient > 0 else '-'}{'' if abs(coefficient) == 1 and power != 0 else abs(coefficient)}{self._variable if power != 0 else ''}{'^'+str(power) if power != 0 and power != 1 else ''}"
        return string.strip(" +").strip()

    def __getitem__(self, item):
        if isinstance(item, (float, int)):
            return self.find_value(item)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Polynomial):
            if self.highest_degree == 0:
                return float(self._dict[0]) == other
            return False
        return self._dict == other._dict

    def __ne__(self, other) -> bool:
        return not (self == other)

    @property
    def variable(self) -> str:
        return variable

    @variable.setter
    def variable(self, new_variable):
        if not isinstance(new_variable, str):
            new_variable = str(new_variable)
        self._variable = new_variable

    @property
    def highest_degree(self) -> int:
        return max(self._dict.keys())

    @property
    def leading_coefficient(self):
        return self._dict[self.highest_degree]

    @abstractmethod
    def find_zeroes(self, remove_complex_numbers=False) -> list:
        raise AttributeError("I don't know how to find the zeroes")

    def find_derivative(self):
        new_dict = {}

        for power, coefficient in self._dict.items():
            if isinstance(coefficient, Trig):
                new_dict[power-1] = coefficient.derivative()
            else:
                new_dict[power-1] = coefficient * power

        return Polynomial(new_dict, variable=self._variable)

    def find_critical_points(self):
        return self.find_derivative().find_zeroes()

    def find_value(self, independent) -> float:
        value = 0

        for power, coefficient in self._dict.items():
            value += coefficient * (independent ** power)
        return value

    def copy(self):
        new_dict = self._dict.copy()
        return Polynomial(new_dict, variable=self._variable)

    def _newton(self, x):
        px = self[x]
        p_x = self.find_derivative()[x]
        return x - px / p_x

    def newtons_method(self, initial_value, less_than=10e-10, output=True):
        i = 1
        xn = initial_value
        print(f"x\u2081 = {' ' if xn >= 0 else ''}{xn:.12f}, f(x\u2081) = {self[xn]:.12f}")
        sub = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        while (abs(self.find_value(xn)) > less_than):
            xn = self._newton(xn)
            i += 1
            if output:
                formatted_i = str(i).translate(sub)
                value = self[xn]
                print(f"x{formatted_i} = {' ' if xn >= 0 else ''}{xn:.12f}, f(x{formatted_i}) = {self[xn]:.12f}")
        return xn


class Linear(Polynomial):
    def __init__(self, factor_dict: dict, **kwargs):
        if len(factor_dict) > 2 or max(dict.keys()) > 1:
            raise AttributeError("A linear equation has 2 powers, the leading power being 1.")
        super().__init__(factor_dict, kwargs)

    def find_zeroes(self, remove_complex_numbers=False):
        try:
            a = self._dict[1]
        except KeyError:
            a = 0
        try:
            b = self._dict[0]
        except KeyError:
            b = 0
        return [b/a]


class Quadratic(Polynomial):
    def __init__(self, factor_dict: dict, **kwargs):
        if len(factor_dict) > 3 or max(dict.keys()) > 2:
            raise AttributeError("A quadratic equation has 3 powers, the leading power being 2.")
        super().__init__(factor_dict, kwargs)

    def find_zeroes(self, remove_complex_numbers=False) -> list:
        try:
            a = self._dict[2]
        except KeyError:
            a = 0
        try:
            b = self._dict[1]
        except KeyError:
            b = 0
        try:
            c = self._dict[0]
        except KeyError:
            c = 0

        in_root = sqrt((b*b) - (4 * a * c))
        positive = (-b + in_root) / (2 * a)
        negative = (-b - in_root) / (2 * a)
        return [i for i in [negative, positive] if isinstance(i, complex)]


class Cubic(Polynomial):
    def __init__(self, factor_dict: dict, **kwargs):
        if len(factor_dict) > 4 or max(dict.keys()) > 3:
            raise AttributeError("A quadratic equation has 4 powers, the leading power being 3.")
        super().__init__(factor_dict, kwargs)

    def find_zeroes(self, remove_complex_numbers=False) -> list:
        try:
            a = self._dict[3]
        except KeyError:
            a = 0
        try:
            b = self._dict[2]
        except KeyError:
            b = 0
        try:
            c = self._dict[1]
        except KeyError:
            c = 0
        try:
            d = self._dict[0]
        except KeyError:
            d = 0

        part1 = Fraction(-(b ** 3), 27*(a**3)) + Fraction(b * c, 6 * a * a) - Fraction(d, 2*a) + sqrt((Fraction(-(b ** 3), 27*(a**3)) + Fraction(b * c, 6 * a * a) - Fraction(d, 2*a))**2)

        return cbrt(part1) + cbrt(part2) + Fraction(b, 3 * a)


if __name__ == "__main__":
    polynomial = Polynomial({3:1,1:-4,0:-1})
    polynomial.newtons_method(1.0, output=True)
    # d1 = {1:1, 0:1} #{4: 1, 3:4, 2:2, 1:2, 0:5}
    # d2 = {2:1, 1:2, 0:1}
    # polynomial = Polynomial(d1)
    # polynomial2 = Polynomial(d2)

    # print(f"'{polynomial}' + '{polynomial2}' = '{polynomial + polynomial2}'")
    # print(polynomial2.find_value(8))
