from __future__ import absolute_import

__author__ = "Len Washington III"
# October 7, 2020
# Least Squares Regression


from ..classes import Fraction
from .statlist import StatList
from .r import R


class Least_Squares_Regression(object):
	"""A class that creates an equation based on the least squares regression of two data sets"""
	def __init__(self, x:StatList, y:StatList):
		"""
		:param washmath.stats.StatList x: A StatList containing the dataset that is considered to be the independent variable
		:param washmath.stats.StatList y: A StatList containing the dataset that is considered to be the dependent variable
		"""
		# self.x = x
		# self.y = y
		# self._r = R(self.x, self.y).getR()
		# self._b1 = self.r * (self.y.standard_deviation / self.x.standard_deviation)
		# self._b0 = self.y.mean - self._b1 * self.x.mean

		self.x = x
		self.y = y

		s_xy = sum([(x1-x.mean) * (y1-y.mean) for x1, y1 in zip(x, y)], start=Fraction(0))
		s_xx = sum([(x1-x.mean) * (x1-x.mean) for x1 in x], start=Fraction(0))
		self._b1 = s_xy / s_xx
		self._b0 = self.y.mean - (self._b1 * self.x.mean)


	@property
	def x(self) -> StatList:
		return self._x

	@x.setter
	def x(self, lst):
		if not isinstance(lst, StatList):
			lst = StatList(lst)
		self._x = lst

	@property
	def y(self) -> StatList:
		return self._y

	@y.setter
	def y(self, lst):
		if not isinstance(lst, StatList):
			lst = StatList(lst)
		self._y = lst

	@property
	def r_squared(self):
		return self.r * self.r

	@property
	def r(self):
		"""
		:rtype: float
		:return: The correlation coefficient of the equation
		"""
		return self._r

	@property
	def slope(self):
		"""
		:rtype: float
		:return: The slope of the linear regression equation
		"""
		return self._b1

	@property
	def y_intercept(self):
		"""
		:rtype: float
		:return: The y-intercept of the linear regression equation
		"""
		return self._b0

	def predict(self, x) -> float:
		"""
		A function that gets a predicted point based on a given dependent variable. 0 would return the y-intercept
		:param float x: The x value that you want to get a prediction for
		:return: The predicted y value based on the equation
		"""
		return self.slope * x + self.y_intercept

	def inverse(self, y) -> float:
		"""
		A function to find the input when given a desired output
		:param y: The desired output
		:return: The necessary input
		"""
		return (y - self.y_intercept) / self.slope

	def __len__(self):
		"""
		:rtype: int
		:return: Returns the length of the data sets
		"""
		return len(self.x)

	def __str__(self):
		"""
		:rtype: str
		:return: A string representation of the equation
		"""
		return f"{self.slope:.4}x + {self.y_intercept:.4}"

	def __repr__(self):
		"""
		:rtype: str
		:return: A string representation of the equation
		"""
		return f"{self.slope:.10}x + {self.y_intercept:.10}"

	def __format__(self, format_spec):
		raise NotImplementedError("Need to implement")
