from abc import ABC, abstractmethod
from ..c_tools import factorial
from ..tools import is_basic_numeric
from .fraction import Fraction


class PI:
    def __float__(self):
        return self()

    def __call__(self) -> float:
        return 3.14159265358979323

    def __truediv__(self, other):
        return Fraction(self, denominator)


class Trig(ABC):
    def __init__(self, x:float, degrees=False):
        self.degrees = degrees
        self.x = x

    @abstractmethod
    def __call__(self):
        pass

    def __float__(self):
        return self()  # Calls __call__

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, x):
        if not is_basic_numeric(x):
            x = float(x)
        if self.degrees:
            x = self.degrees_to_radians(x)
        self._x = x

    @property
    def degrees(self) -> bool:
        return self._degrees

    @degrees.setter
    def degrees(self, value):
        if not isinstance(value, bool):
            value = bool(value)
        self._degrees = value

    @abstractmethod
    def derivative(self):
        pass

    def radians_to_degrees(self):
        return self._x * 180 / float(PI())

    @staticmethod
    def degrees_to_radians(self, degrees):
        return degrees * float(PI()) / 180


class SIN(Trig):
    def __init__(self, x:float, degrees=False):
        super().__init__(x, degrees)

    def __repr__(self):
        return f"sin({self.x}) = {self()}"

    def __call__(self, x=None) -> float:
        if x is None and hasattr(self, "_summation"):
            return self._summation
        if x is not None and self.degrees:
            x = self.degrees_to_radians(x)
        x = self._x if x is None else x

        if x > 2 * PI:
            x %= (2*PI)

        self._summation = 0

        for n in range(33):
            numerator = ((-1) ** n) * (x ** (2*n + 1))
            self._summation += numerator / factorial(2*n + 1)

        return self._summation

    def derivative(self):
        return COS(self.x, self.degrees)


class COS(Trig):
    def __init__(self, x:float, degrees=False):
        super().__init__(x, degrees)

    def __repr__(self):
        return f"cos({self.x}) = {self()}"

    def __call__(self, x=None) -> float:
        if x is not None and self.degrees:
            x = self.degrees_to_radians(x)
        x = self._x if x is None else x

        if x > 2 * PI:
            x %= (2*PI)

        summation = 0

        for k in range(33):
            numerator = ((-1) ** k) * (x ** (2*k))
            summation += numerator / factorial(2 * k)

        return summation

    def derivative(self):
        derivative = -SIN(self.x, self.degrees)
        #TODO: Implement polynomials as x inputs
        #TODO: Implement powers
        return derivative


class TAN(Trig):
    def __init__(self, x:float, degrees=False):
        super().__init__(x, degrees)

    def __repr__(self):
        return f"tan({self.x}) = {self()}"

    def __call__(self, x=None) -> float:
        if x is not None and self.degrees:
            x = self.degrees_to_radians(x)
        x = self._x if x is None else x

        if x > 2 * PI:
            x %= (2*PI)

        # Copy the full summation of sine, then calculate full of cos, then do division of summations

        return float(SIN(x)() / COS(x)(x))

    def derivative(self):
        return SEC(self.x, self.degrees) ** 2


class CSC(Trig):
    def __init__(self, x:float, degrees=False):
        super().__init__(x, degrees)

    def __repr__(self):
        return f"csc({self.x}) = {self()}"

    def __call__(self, x=None) -> float:
        if x is not None and self.degrees:
            x = self.degrees_to_radians(x)
        x = self._x if x is None else x

        if x > 2 * PI:
            x %= (2*PI)

        summation = 0

        for n in range(33):
            numerator = ((-1) ** n) * (x ** (2*n + 1))
            summation += numerator / factorial(2*n + 1)

        return 1/summation

    def derivative(self):
        return COS(self.x, self.degrees)


class SEC(Trig):
    def __init__(self, x:float, degrees=False):
        super().__init__(x, degrees)

    def __repr__(self):
        return f"sec({self.x}) = {self()}"

    def __call__(self, x=None) -> float:
        if x is not None and self.degrees:
            x = self.degrees_to_radians(x)
        x = self._x if x is None else x

        if x > 2 * PI:
            x %= (2*PI)

        summation = 0

        for k in range(33):
            numerator = ((-1) ** k) * (x ** (2*k))
            summation += numerator / factorial(2 * k)

        return 1/summation

    def derivative(self):
        derivative = SEC(self.x, self.degrees) * TAN(self.x, self.degrees)
        return derivative


class ATAN(Trig):
    def __init__(self, x:float, degrees=False):
        super().__init__(x, degrees)

    def __repr__(self):
        return f"sin({self.x}) = {self()}"

    def __call__(self, x=None) -> float:
        if x is not None and self.degrees:
            x = self.degrees_to_radians(x)
        x = self._x if x is None else x

        if x > 2 * PI:
            x %= (2*PI)

        summation = 0

        for n in range(33):
            numerator = ((-1) ** n) * (x ** (2*n + 1))
            summation += numerator / (2*n + 1)

        return summation

    def derivative(self):
        return COS(self.x, self.degrees)


class E:
    def __init__(self, x:float):
        self._x = x

    def __repr__(self):
        return f"e^{self._x} = {float(self)}"

    def __float__(self):
        return float(self())

    def __call__(self, x=None):
        if x is None and hasattr(self, "_summation"):
            return self._summation
        x = self._x if x is None else x

        self._summation = 1

        for n in range(1, 50):
            self._summation += x ** n / factorial(n)

        return self._summation
