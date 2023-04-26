from __future__ import absolute_import

__author__ = "Len Washington III"

from .statlist import StatList
from .lsr import Least_Squares_Regression
from ..classes import Fraction


class Residual(object):
	"""A class that finds the residuals of a Least Squares Regression equation"""
	def __init__(self, x:StatList, y:StatList, prediction:Least_Squares_Regression):
		"""
		:param StatList x:
		:param StatList y:
		:param Least_Squares_Regression prediction:
		"""
		self.x = x
		self.y = y
		self.prediction = prediction
		self._residual = (self._diff_sum() / (len(y)-2)) ** 0.5

	@property
	def residual(self):
		"""
		:rtype: float
		:return: The residual of the equation
		"""
		return self._residual

	@property
	def sse(self) -> Fraction:
		# return sum([(yi - self.prediction.y_intercept - (self.prediction.slope*xi))**2 for xi, yi in zip(self.x, self.y)], start=Fraction(0))
		return sum([(yi - self.prediction.predict(xi))**2 for xi, yi in zip(self.x, self.y)], start=Fraction(0))

	def _diff_sum(self) -> Fraction:
		"""
		:rtype: float
		:return: The difference of sums between the actual dependent variables and the predicted variables
		"""
		diff_sum = Fraction(0)
		predictions = [self.prediction.predict(x) for x in self.x]
		self._residuals = [None] * len(self)
		for (y, predict) in zip(self.y, predictions):
			point = Fraction(y) - Fraction(predict)
			diff_sum += point
			self.residuals.append(point)
		return diff_sum

	@property
	def residuals(self):
		return self._residuals

	def __str__(self):
		"""
		:rtype: str
		:return: The string interpretation of the residual
		"""
		return f"The residual is {self.residual*100:.4}%"

	def __len__(self):
		"""
		:rtype: int
		:return: The length of the data sets
		"""
		return len(self.x)

	def __float__(self):
		"""
		:rtype: float
		:return: The residual if the object needs to be turned into a float
		"""
		return self.residual

	@classmethod
	def fromTwoLists(cls, x:list, y:list):
		"""
		:param list x:
		:param list y:
		:rtype: stats.residual.Residual
		"""
		x = StatList(x)
		y = StatList(y)
		return cls.fromTwoStatLists(x, y)

	@classmethod
	def fromTwoStatLists(cls, x:StatList, y:StatList):
		"""
		:param stats.StatList.StatList x:
		:param stats.StatList.StatList y:
		:rtype: stats.residual.Residual
		"""
		return cls(x, y, Least_Squares_Regression(x, y))

	@classmethod
	def create(cls):
		"""
		:rtype: stats.residual.Residual
		:return: Finds the residual of a least squares regression of two data sets given by the user
		"""
		x_lst, y_lst = [], []
		while True:
			element = input("Input the next element in the (x,y) form. Enter nothing to finish. ").replace("(", "").replace(")", "")
			x, y = element.split(",")
			if x != "":
				x_lst.append(float(element))
			if y != "":
				y_lst.append(float(element))
			if element == "":
				break
		x_lst, y_lst = StatList(x_lst), StatList(y_lst)
		return cls(x_lst, y_lst, Least_Squares_Regression(x_lst, y_lst))
