from numpy import lcm, int32, int64, gcd
from numpy.core._exceptions import UFuncTypeError, _UFuncNoLoopError
from warnings import warn
from ..tools import is_basic_numeric


class Number:
	def __init__(self, value):
		self.value = value
		self._upper_pow = 1
		self._lower_pow = 1

	@property
	def value(self):
		return self._value ** (self._upper_pow / self._lower_pow)

	@value.setter
	def value(self, value):
		self._value = value

	@property
	def has_radical(self) -> bool:
		return self.get_radical != 1

	@property
	def get_radical(self):
		return self._lower_pow

	# region Operator Overloads
	def __int__(self):
		return int(self.value)

	def __float__(self):
		return float(self.value)

	def __add__(self, other):
		if isinstance(other, Number):
			return Number(self.value + other.value)
		elif isinstance(other, (int, float)):
			return Number(self.value + other)

		raise NotImplementedError("Haven't implemented adding numbers")

	def __mul__(self, other):
		if isinstance(other, (float, int)):
			number = Number(self.value * other)
			number._upper_pow = self._upper_pow
			number._lower_pow = self._lower_pow
			return number
		elif isinstance(other, Number):
			number = Number(other.value * self.value)
			if self._upper_pow != 1 and self._lower_pow != 1 and other._upper_pow != 1 and self._lower_pow != 1:
				powers = Fraction(self._upper_pow, self._lower_pow)
				other_powers = Fraction(other._upper_pow, other._lower_pow)
				combined_powers = powers * other_powers
				number._upper_pow = combined_powers.numerator
				number._lower_pow = combined_powers.denominator
			return number

	def __pow__(self, power, modulo=None):
		if isinstance(power, float):
			power = Fraction(power)

		if isinstance(power, Fraction):
			self._upper_pow *= power.numerator
			self._lower_pow *= power.denominator
		else:
			self._upper_pow *= power

		_gcd = gcd(self._upper_pow, self._lower_pow)
		if _gcd != 1:
			self._upper_pow /= _gcd
			self._lower_pow /= _gcd

	def __repr__(self):
		if self._upper_pow == 1 and self._lower_pow == 1:
			return f"{self.value}"
		upper_power = self._upper_pow if self._upper_pow != 1 else 1
		lower_power = self._lower_pow if self._lower_pow != 1 else 1

	def __abs__(self):
		number = Number(abs(self.value))
		number._upper_pow = self._upper_pow
		number._lower_pow = self._lower_pow
		return number


# endregion


class Fraction(object):
	REGEX = r"([0-9]+.?[0-9]+)\s?/\s?([0-9]+.?[0-9]+)"

	def __init__(self, numerator, denominator=1, auto_reduce=True, **kwargs):
		"""
		:param bool persistent_denominator: If the denominator should be kept as is if the numerator is 0. Default is False.
		:param bool auto_reduce: If the fraction should be automatically reduced.
		"""
		self._allowed_to_reduce = False
		self.auto_reduce = auto_reduce
		self._persistent_denominator = kwargs.get("persistent_denominator", False)

		if isinstance(denominator, Fraction):
			self.numerator = numerator * denominator.denominator
		else:
			self.numerator = numerator
		self._allowed_to_reduce = True
		if hasattr(self, "_denominator"):
			try:
				self.denominator *= denominator.denominator  # The numerator was a fraction, and the new denominator needs to be multiplied by the old one.
			except TypeError as e:
				self.denominator = denominator * self._denominator
		else:
			self.denominator = denominator

	# region Operator Overloads
	def __add__(self, other):
		if isinstance(other, Fraction):
			if (self.denominator == other.denominator):
				return Fraction(self.numerator + other.numerator, self.denominator, auto_reduce=self.auto_reduce)
			else:
				newDenominator = self.denominator * other.denominator
				newSelf = self.numerator * other.denominator
				newOther = other.numerator * self.denominator
				return Fraction(newSelf + newOther, newDenominator, auto_reduce=self.auto_reduce)  # Now they have matching denominators
		elif isinstance(other, (int, float)):
			newNumerator = other * self.denominator
			return Fraction(newNumerator + self.numerator, self.denominator)

	def __iadd__(self, other):
		if isinstance(other, Fraction):
			if (self.denominator == other.denominator):
				self.numerator += other.numerator
			else:
				self.numerator = (self.numerator * other.denominator) + (other.numerator * self.denominator)
				self.denominator *= other.denominator
		elif isinstance(other, (int, float)):
			newNumerator = other * self.denominator
			self.numerator += newNumerator
		return self

	def __sub__(self, other):
		if isinstance(other, Fraction):
			if (self.denominator == other.denominator):
				return Fraction(self.numerator - other.numerator, self.denominator)
			else:
				newDenominator = self.denominator * other.denominator
				newSelf = self.numerator * (newDenominator / self.denominator)
				newOther = other.numerator * (newDenominator / other.denominator)
				return Fraction(newSelf - newOther, newDenominator)
		elif isinstance(other, (int, float)):
			newNumerator = other * self.denominator
			return Fraction(self.numerator - newNumerator, self.denominator)

	def __isub__(self, other):
		if isinstance(other, Fraction):
			if (self.denominator == other.denominator):
				self.numerator -= other.numerator
			else:
				newDenominator = lcm(self.denominator, other.denominator)
				newOther = other.numerator * (other.denominator / newDenominator)
				self.numerator -= newOther
		elif isinstance(other, (int, float)):
			newNumerator = other * self.denominator
			self.numerator -= newNumerator
		return self

	def __mul__(self, other):
		if isinstance(other, Fraction):
			return Fraction(self.numerator * other.numerator, self.denominator * other.denominator, auto_reduce=self.auto_reduce)
		elif isinstance(other, (int, float)):
			return Fraction(self.numerator * other, self.denominator, self.auto_reduce)

	def __imul__(self, other):
		if isinstance(other, Fraction):
			self._allowed_to_reduce = False
			self.numerator *= other.numerator
			self._allowed_to_reduce = True
			self.denominator *= other.denominator
		elif isinstance(other, (int, float)):
			self.numerator *= other
		return self

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
		return self

	def __pow__(self, power, modulo=None):
		if power == 0:
			if self.numerator == 0:
				raise Exception("Cannot raise 0 to the zeroth power.")
			return Fraction(1)
		elif power == 1:
			return self.copy()
		elif power > 0:
			newNumerator = self.numerator ** power
			newDenominator = self.denominator ** power
			return Fraction(newNumerator, newDenominator)
		else:
			return Fraction(self.denominator, self.numerator) ** -power

	def __ipow__(self, power, modulo=None):
		if self < 0 and power < 1:
			raise ValueError("Can't take the root of a negative fraction.")
		if power == 0:
			if self.numerator == 0:
				raise Exception("Cannot raise 0 to the zeroth power.")
			self.numerator = self.denominator = 1
			return self
		elif power == 1:
			return self
		elif power > 0:
			self._allowed_to_reduce = False
			self.numerator **= power
			self._allowed_to_reduce = True
			self.denominator **= power
			return self
		else:
			numerator = self.denominator ** power
			denominator = self.numerator ** power
			self.numerator = numerator
			self.denominator = denominator
			return self

	def __float__(self):
		return self.numerator / self.denominator

	def __int__(self):
		return int(float(self))

	def __abs__(self):
		return Fraction(abs(self.numerator), self.denominator)

	def __pos__(self):
		return Fraction(abs(self.numerator), self.denominator)

	def __neg__(self):
		return Fraction(-abs(self.numerator), self.denominator)

	def __str__(self):
		return repr(self)

	# return f"{self.numerator:,}/{self.denominator:,}"

	def __repr__(self):
		if self.numerator == 0:
			return "0"
		if self.denominator == 1:
			return str(self.numerator)
		return f"{self.numerator}/{self.denominator} ({float(self)})"

	def __bool__(self):
		return bool(self.numerator)

	def __lt__(self, other):
		if isinstance(other, Fraction):
			if self.denominator == other.denominator:
				return self.numerator < other.numerator
			else:
				try:
					newDenominator = lcm(self.denominator, other.denominator)
				except _UFuncNoLoopError:
					newDenominator = self.denominator * other.denominator
				newSelf = self.numerator * (newDenominator / self.denominator)
				newOther = other.numerator * (newDenominator / other.denominator)
				return newSelf < newOther
		return float(self) < other

	def __gt__(self, other):
		if isinstance(other, Fraction):
			if self.denominator == other.denominator:
				return self.numerator > other.numerator
			else:
				try:
					newDenominator = lcm(self.denominator, other.denominator)
				except _UFuncNoLoopError:
					newDenominator = self.denominator * other.denominator
				newSelf = self.numerator * (newDenominator / self.denominator)
				newOther = other.numerator * (newDenominator / other.denominator)
				return newSelf > newOther
		return float(self) > other

	def __eq__(self, other):
		if other is None: return False
		if isinstance(other, int):
			return int(self) == other
		elif isinstance(other, Fraction):
			if self.denominator == other.denominator:
				return self.numerator == other.numerator
			else:
				newDenominator = lcm(self.denominator, other.denominator)
				newSelf = self.numerator * (newDenominator / self.denominator)
				newOther = other.numerator * (newDenominator / other.denominator)
				return newSelf == newOther
		elif isinstance(other, bool):
			return bool(self) == other
		return float(self) == other

	def __le__(self, other):
		return (self < other) or (self == other)

	def __ge__(self, other):
		return (self > other) or (self == other)

	def __ne__(self, other):
		return not (self == other)

	def __hash__(self):
		return hash((self.numerator, self.denominator))

	def __format__(self, format_spec):
		if format_spec == ",":
			if self.numerator == 0:
				return "0"
			if self.denominator == 1:
				return f"{self.numerator:,}"
			return f"{self.numerator:,}/{self.denominator:,}"
		return format(float(self), format_spec)

	def __round__(self, ndigits=0):
		return round(float(self), ndigits)

	# endregion

	@property
	def numerator(self):
		return self._numerator

	@numerator.setter
	def numerator(self, numerator):
		if not is_basic_numeric(numerator) and not isinstance(numerator, (Number, Fraction)):
			raise AttributeError(f"The numerator must be a washmath.Number, not {type(numerator).__name__}")

		if isinstance(numerator, Number):
			numerator = numerator.value

		if isinstance(numerator, (int, float)):
			self._numerator = numerator
		# numerator = Number(int)
		if isinstance(numerator, Fraction):
			self._denominator = numerator.denominator * (self.denominator if hasattr(self, "_denominator") else 1)
			self._numerator = numerator.numerator
		elif isinstance(numerator, Number):
			self._numerator = numerator
		if self.auto_reduce:
			self.reduce()

	@property
	def denominator(self):
		return self._denominator

	@denominator.setter
	def denominator(self, denominator):
		# if not is_basic_numeric(denominator):
		if not is_basic_numeric(denominator) and not isinstance(denominator, (Number, Fraction)):
			raise AttributeError(f"The denominator must be a washmath.Number, not {type(denominator).__name__}")
		if denominator == 0:
			raise ZeroDivisionError("0 cannot be the denominator of a function")

		if denominator < 0:
			denominator *= -1
			self._numerator *= -1

		if isinstance(denominator, Number):
			denominator = denominator.value

		if isinstance(denominator, (int, float)):
			self._denominator = denominator
		# denominator = Number(denominator)
		if isinstance(denominator, Fraction):
			self._numerator *= denominator.denominator
			self._denominator = denominator.numerator
		elif isinstance(denominator, Number):
			whole_denominator = denominator ** denominator.get_radical
			self._numerator *= denominator
			self._denominator = whole_denominator
		if self.auto_reduce:
			self.reduce()

	def copy(self):
		return Fraction(self.numerator, self.denominator, auto_reduce=self.auto_reduce)

	def reduce(self):
		def equals(num: float) -> bool:
			return int(num) == num

		if not self._allowed_to_reduce:
			return

		while self.numerator % 1 != 0 or self.denominator % 1 != 0:
			self._numerator *= 10
			self._denominator *= 10

		try:
			factor = gcd(int(self.numerator), int(self.denominator))
			if (factor != 1 and factor != 0) and not (self._numerator == 0 and self._persistent_denominator):
				self._numerator /= factor
				self._denominator /= factor
		except UFuncTypeError as e:
			warn(str(e))

		if equals(self.numerator):
			self._numerator = int(self.numerator)

		if equals(self.denominator):
			self._denominator = int(self.denominator)

		return self

	@property
	def is_whole(self) -> bool:
		"""Returns whether the fraction is a whole number or not"""
		return self.denominator == 1

	def __invert__(self):
		return self.inverse

	@property
	def inverse(self):
		return Fraction(self.denominator, self.numerator)

	@property
	def to_tex(self) -> str:
		return f"\\frac{{{self.numerator:,}}}{{{self.denominator:,}}}"


if __name__ == "__main__":
	frac = Fraction(1, 2)
	frac2 = Fraction(3.08, 4)
	print(frac2)
	print(f"{frac} - {frac2} = {frac2 ** 2}")
