from ..class_tools import is_numeric
from .fraction import Fraction, Number


def is_numeric_but_not_fraction(number):
	if not is_numeric(number) and not isinstance(number, Number):
		return False
	if not isinstance(number, (Fraction, Number)):
		return Fraction(number)
	return number


class Vector(object):
	def __init__(self, x, y, z=0):
		self.x = x  # TODO: Remove this automatic conversion
		self.y = y
		self.z = z

	# region Properties
	@property
	def x(self) -> Fraction:
		return self._x

	@x.setter
	def x(self, x):
		x = is_numeric_but_not_fraction(x)
		if x is False and not isinstance(x, Fraction):  # Because is a fraction is 0, it comes out as false
			raise ValueError(f"The x component of a vector must be numeric, not {type(x).__name__}")
		self._x = x

	@x.deleter
	def x(self):
		self._x = Fraction(0)

	@property
	def y(self) -> Fraction:
		return self._y

	@y.setter
	def y(self, y):
		y = is_numeric_but_not_fraction(y)
		if y is False and not isinstance(y, Fraction):  # Because is a fraction is 0, it comes out as false
			raise ValueError(f"The y component of a vector must be numeric, not {type(y).__name__}")
		self._y = y

	@y.deleter
	def y(self):
		self._y = Fraction(0)

	@property
	def z(self) -> Fraction:
		return self._z

	@z.setter
	def z(self, z):
		z = is_numeric_but_not_fraction(z)
		if z is False and not isinstance(z, Fraction):  # Because is a fraction is 0, it comes out as false
			raise ValueError(f"The z component of a vector must be numeric, not {type(z).__name__}")
		self._z = z

	@z.deleter
	def z(self):
		self._z = Fraction(0)

	@property
	def magnitude(self) -> Fraction:
		return self.magnitude_squared ** 0.5

	@property
	def magnitude_squared(self) -> Fraction:
		return self.x ** 2 + self.y ** 2 + self.z ** 2

	@property
	def unit_vector(self):
		"""
		Returns a vector with magnitude 1 in the same direction as this vector
		:rtype: Vector
		"""
		return self * Fraction(1, self.magnitude)
	# endregion

	# region Operation overloads

	def __add__(self, other):
		if isinstance(other, Vector):
			x = self.x + other.x
			y = self.y + other.y
			z = self.z + other.z
			return Vector(x, y, z)
		raise NotImplementedError()

	def __sub__(self, other):
		if isinstance(other, Vector):
			x = self.x - other.x
			y = self.y - other.y
			z = self.z - other.z
			return Vector(x, y, z)
		raise NotImplementedError()

	def __mul__(self, other):
		if isinstance(other, Vector):
			return self.dot_product(other)
		elif is_numeric(other):
			x = self.x * other
			y = self.y * other
			z = self.z * other
			return Vector(x, y, z)

	def __eq__(self, other):
		if not isinstance(other, Vector):
			return False
		return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

	def __ne__(self, other):
		return not (self == other)

	def __neg__(self):
		return Vector(-self.x, -self.y, -self.z)

	def __repr__(self):
		return f"<{repr(self.x)}, {repr(self.y)}, {repr(self.z)}>"
	# endregion

	def dot_product(self, other):
		if not isinstance(other, Vector):
			raise ValueError(f"The dot product takes two vectors, not a vector and a {type(other).__name__}.")
		return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

	def angle_between(self, other):
		if not isinstance(other, Vector):
			raise ValueError(f"Finding the angle between two vectors requires two vectors, not a vector and a {type(other).__name__}.")
		from numpy import arccos
		cos_theta = self.dot_product(other) / (self.magnitude * other.magnitude)
		return arccos(cos_theta)

	def comp(self, other) -> Fraction:
		"""
		Finds the scalar projection of one vector onto another. It should be read as "the scalar projection of other onto self" OR comp(self) other if looking at the calculus notation

		:param Vector other:
		"""
		if not isinstance(other, Vector):
			raise ValueError(f"The given argument for finding the projection of a vector on another vector requires two vectors, not a vector and a {type(other).__name__}.")
		return Fraction(self.dot_product(other), self.magnitude)

	def projection(self, other):
		"""
		Finds the projection of one vector onto another. It should be read as "the projection of other onto self" OR proj(self) other if looking at the calculus notation

		:param Vector other:
		:rtype Vector:
		"""
		if not isinstance(other, Vector):
			raise ValueError(f"The given argument for finding the projection of a vector on another vector requires two vectors, not a vector and a {type(other).__name__}.")

		return self.unit_vector * self.comp(other)

	def cross_product(self, other):
		"""

		:param Vector other:
		:rtype: Vector
		"""
		x = (self.y * other.z) - (self.z * other.y)
		y = (self.z * other.x) - (self.x * other.z)
		z = (self.x * other.y) - (self.y * other.x)
		return Vector(x, y, z)
