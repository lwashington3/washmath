from numpy import lcm, int32, int64
from .c_tools import gcd


def is_numeric(obj):
    return isinstance(obj, (int, float, Fraction, int32, int64))


class Fraction(object):
    REGEX = r"([0-9]+.?[0-9]+)\s?/\s?([0-9]+.?[0-9]+)"  # ECON 423
    def __init__(self, numerator, denominator=1):
        self._allowed_to_reduce = False
        self.numerator = numerator
        self.denominator = denominator
        self._allowed_to_reduce = True
        self.reduce()

    def __add__(self, other):
        if isinstance(other, Fraction):
            if(self.denominator == other.denominator):
                return Fraction(self.numerator + other.numerator, self.denominator)
            else:
                newDenominator = self.denominator * other.denominator
                newSelf = self.numerator * other.denominator
                newOther = other.numerator * self.denominator
                return Fraction(newSelf + newOther, newDenominator)  # Now they have matching denominators
        elif isinstance(other, (int, float)):
            newNumerator = other * self.denominator
            return Fraction(newNumerator + self.numerator, self.denominator)

    def __iadd__(self, other):
        if isinstance(other, Fraction):
            if(self.denominator == other.denominator):
                self.numerator += other.numerator
            else:
                self.numerator = (self.numerator * other.denominator) + (other.numerator * self.denominator)
                self.denominator * other.denominator
        elif isinstance(other, (int, float)):
            newNumerator = other * self.denominator
            self.numerator += newNumerator
        return self

    def __sub__(self, other):
        if isinstance(other, Fraction):
            if(self.denominator == other.denominator):
                return Fraction(self.numerator - other.numerator, self.denominator)
            else:
                newDenominator = self.denominator * other.denominator
                newSelf = self.numerator * (newDenominator / self.denominator)
                newOther = other.numerator * (newDenominator / other.denominator)
                return Fraction(newSelf - newOther, newDenominator)
        elif isinstance(other, (int, float)):
            newNumerator = other * self.denominator
            return Fraction(newNumerator - self.numerator, self.denominator)

    def __isub__(self, other):
        if isinstance(other, Fraction):
            if(self.denominator == other.denominator):
                self.numerator -= other.numerator
            else:
                newDenominator = lcm(self.denominator, other.denominator)
                newOther = other.numerator * (other.denominator / newDenominator)
                self.numerator -= newOther
        elif isinstance(other, (int, float)):
            newNumerator = other * self.denominator
            self.numerator -= newNumerator

    def __mul__(self, other):
        if isinstance(other, Fraction):
            return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)
        elif isinstance(other, (int, float)):
            return Fraction(self.numerator * other, self.denominator)

    def __imul__(self, other):
        if isinstance(other, Fraction):
            self.numerator *= other.numerator
            self.denominator *= other.denominator
        elif isinstance(other, (int, float)):
            self.numerator *= other

    def __truediv__(self, other):
        if isinstance(other, Fraction):
            return self * Fraction(other.denominator, other.numerator)
        elif isinstance(other, (float, int)):
            if self.numerator % other == 0:
                return Fraction(self.numerator / other, self.denominator)
            return Fraction(self.numerator, self.denominator * other)

    def __idiv__(self, other):
        if isinstance(other, Fraction):
            self.numerator *= other.denominator
            self.denominator *= other.numerator
        elif isinstance(other, (float, int)):
            if self.numerator % other == 0:
                self.numerator /= other
            else:
                self.denominator *= other

    def __pow__(self, power, modulo=None):
        newNumerator = self.numerator ** power
        newDenominator = self.denominator ** power
        return Fraction(newNumerator, newDenominator)

    def __ipow__(self, other, modulo=None):
        self._numerator **= other
        self._denominator **= other
        return self

    def __float__(self):
        return self.numerator / self.denominator

    def __int__(self):
        return int(float(self))

    def __abs__(self):
        return Fraction(abs(self.numerator), abs(self.denominator))

    def __pos__(self):
        return Fraction(abs(self.numerator), self.denominator)

    def __neg__(self):
        return Fraction(-abs(self.numerator), self.denominator)

    def __str__(self):
        return f"{self.numerator:,}/{self.denominator:,}"

    def __repr__(self):
        return f"{self.numerator}/{self.denominator}"

    def __lt__(self, other):
        if isinstance(other, Fraction):
            if self.denominator == other.denominator:
                return self.numerator < other.numerator
            else:
                newDenominator = lcm(self.denominator, other.denominator)
                newSelf = self.numerator * (self.denominator / newDenominator)
                newOther = other.numerator * (other.denominator / newDenominator)
                return newSelf < other
        return float(self) < other

    def __gt__(self, other):
        if isinstance(other, Fraction):
            if self.denominator == other.denominator:
                return self.numerator > other.numerator
            else:
                newDenominator = lcm(self.denominator, other.denominator)
                newSelf = self.numerator * (self.denominator / newDenominator)
                newOther = other.numerator * (other.denominator / newDenominator)
                return newSelf > other
        return float(self) > other

    def __le__(self, other):
        if isinstance(other, Fraction):
            if self.denominator == other.denominator:
                return self.numerator <= other.numerator
            else:
                newDenominator = lcm(self.denominator, other.denominator)
                newSelf = self.numerator * (self.denominator / newDenominator)
                newOther = other.numerator * (other.denominator / newDenominator)
                return newSelf <= other
        return float(self) <= other

    def __ge__(self, other):
        if isinstance(other, Fraction):
            if self.denominator == other.denominator:
                return self.numerator >= other.numerator
            else:
                newDenominator = lcm(self.denominator, other.denominator)
                newSelf = self.numerator * (self.denominator / newDenominator)
                newOther = other.numerator * (other.denominator / newDenominator)
                return newSelf >= other
        return float(self) >= other

    def __eq__(self, other):
        if isinstance(other, int):
            return float(self) == other
        elif isinstance(other, Fraction):
            if self.denominator == other.denominator:
                return self.numerator == other.numerator
            else:
                newDenominator = lcm(self.denominator, other.denominator)
                newSelf = self.numerator * (self.denominator / newDenominator)
                newOther = other.numerator * (other.denominator / newDenominator)
                return newSelf == newOther
        return float(self) == other

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.numerator, self.denominator))

    def __round__(self, ndigits=0):
        return round(float(self), ndigits)

    @staticmethod
    def equals(num:float) -> bool:
        return int(num) == num

    @property
    def numerator(self) -> int:
        return self._numerator

    @numerator.setter
    def numerator(self, numerator):
        if not is_numeric(numerator):
            raise AttributeError(f"The numerator must be a number, not {numerator.__name__}")
        self._numerator = numerator
        self.reduce()

    @property
    def denominator(self):
        return self._denominator

    @denominator.setter
    def denominator(self, denominator):
        if not is_numeric(denominator):
            raise AttributeError(f"The denominator must be a number, not {denominator.__name__}")
        if denominator == 0:
            raise ZeroDivisionError("0 cannot be the denominator of a function")

        if denominator < 0:
            denominator *= -1
            self._numerator *= -1
        self._denominator = denominator
        self.reduce()

    def reduce(self):
        if not self._allowed_to_reduce:
            return
        if self.equals(self.numerator):
            self._numerator = int(self._numerator)
        if self.equals(self.denominator):
            self._denominator = int(self._denominator)

        mult = 1
        while not (self.equals(self.numerator*mult) and self.equals(self.denominator*mult)):
            mult += 1

        self._numerator = int(self.numerator * mult)
        self._denominator = int(self.denominator * mult)

        factor = gcd(self.numerator, self.denominator)
        if factor != 1 and factor != 0:
            self.numerator /= factor
            self.denominator /= factor

        return self


if __name__ == "__main__":
    frac = Fraction(1, 2)
    frac2 = Fraction(3.08, 4)
    print(frac2)
    frac.reduce()
    print(f"{frac} - {frac2} = {frac2 ** 2}")
