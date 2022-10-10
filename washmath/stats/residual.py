from __future__ import absolute_import

__author__ = "Len Washington III"

from .statlist import StatList
from .lsr import Least_Squares_Regression


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
		self.residual = (self._diff_sum() / (len(y)-2)) ** 0.5

	def getResidual(self):
		"""
		:rtype: float
		:return: The residual of the equation
		"""
		return self.residual

	def _diff_sum(self):
		"""
		:rtype: float
		:return: The difference of sums between the actual dependent variables and the predicted variables
		"""
		sum = 0.0
		y_lstt = self.y
		predict_lstt = [self.prediction.slope * x + self.prediction.y_intercept for x in self.x]
		self.residuals = []
		for (y, predict) in zip(y_lstt, predict_lstt):
			sum += y - predict
			self.residuals.append(point)
		return sum

	def getResidualPoints(self):
		return self.residuals

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
