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
		self.x = x
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

	def __abs__(self):
		return Vector(abs(self.x), abs(self.y), abs(self.z))

	def __neg__(self):
		return Vector(-self.x, -self.y, -self.z)

	def __repr__(self):
		return f"<{repr(self.x)}, {repr(self.y)}, {repr(self.z)}>"
	# endregion

	def dot_product(self, other):
		if not isinstance(other, Vector):
			raise ValueError(f"The dot product takes two vectors, not a vector and a {type(other).__name__}.")
		return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

	def angle_between(self, other, in_radians=True):
		if not isinstance(other, Vector):
			raise ValueError(f"Finding the angle between two vectors requires two vectors, not a vector and a {type(other).__name__}.")
		from numpy import arccos
		cos_theta = self.dot_product(other) / (self.magnitude * other.magnitude)
		angle = arccos(cos_theta)
		if in_radians:
			return angle
		from math import pi
		return angle * (180 / pi)

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

		# return self.unit_vector * self.comp(other)
		return self * Fraction(self.dot_product(other), self.magnitude_squared)

	def cross_product(self, other):
		"""

		:param Vector other:
		:rtype: Vector
		"""

		x = (self.y * other.z) - (self.z * other.y)
		y = (self.z * other.x) - (self.x * other.z)
		z = (self.x * other.y) - (self.y * other.x)
		return Vector(x, y, z)

	def volume_of_para(self, b, c) -> Fraction:
		"""
		:param Vector b:
		:param Vector c:

		"""
		# v = |a * (bxc)|
		if not isinstance(b, Vector):
			raise ValueError(f"The first given argument finding the volume must be a Vector, not a {type(b).__name__}")
		if not isinstance(c, Vector):
			raise ValueError(f"The second given argument finding the volume must be a Vector, not a {type(c).__name__}")

		bc = b.cross_product(c)
		return abs(self.dot_product(bc))

	def is_r1(self) -> bool:
		"""
		Checks if the vector is R1
		"""
		in_plane_list = [bool(i) for i in (self.x, self.y, self.z)]
		return in_plane_list.count(True) == 1

	def is_r2(self) -> bool:
		"""
		Checks if the vector is R2
		"""
		in_plane_list = [bool(i) for i in (self.x, self.y, self.z)]
		return in_plane_list.count(True) == 2

	def is_r3(self) -> bool:
		"""Checks if the vector is R3"""
		return bool(self.x) and bool(self.y) and bool(self.z)

	def scalar_equation_of_plane(self, normal) -> str:
		"""

		:param Vector normal: The vector orthogonal to the plane
		"""
		if not isinstance(normal, Vector):
			raise ValueError(f"The normal vector must be a Vector, not a {type(b).__name__}")
		a = normal.x
		b = normal.y
		c = normal.z

		summation = -((a*self.x) + (b*self.y) + (c*self.z))  # TODO: Simplify if possible

		return f"{a}x + {b}y + {c}z = {summation}"

	def equation_of_plane(self, q, r) -> str:
		"""
		:param Vector q: The q point on the plane
		:param Vector r: The r point on the plane
		"""
		if not isinstance(q, Vector):
			raise ValueError(f"The first given argument finding the volume must be a Vector, not a {type(q).__name__}")
		if not isinstance(r, Vector):
			raise ValueError(f"The second given argument finding the volume must be a Vector, not a {type(r).__name__}")
		a = q - self
		b = r - self
		normal_vector = a.cross_product(b)
		return self.scalar_equation_of_plane(normal_vector)

	# region Class methods
	@classmethod
	def from_angle(cls, magnitude, angle, in_radians=True):
		"""
		Creates a 2-D vector given a magnitude and angle
		:param float magnitude: The magnitude of the vector
		:param float angle: The angle of the vector with the positive x-axis
		:param bool in_radians: If the given angle is in radians or not. If not, the angle will be inferred as degrees.
		"""
		from .trig import SIN, COS

		if not in_radians:
			from .trig import PI
			angle = (PI() / 180) * angle

		x = magnitude * COS(angle)()
		y = magnitude * SIN(angle)()
		return cls(x, y)

	# endregion
