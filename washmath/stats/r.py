from __future__ import absolute_import


from .statlist import StatList


class R(object):
	"""A class that gets the correlation coefficient of two StatLists"""
	def __init__(self, x_lst:StatList, y_lst:StatList):
		"""
		:param StatList x_lst: A StatList containing the dataset that is considered to be the independent variable
		:param StatList y_lst: A StatList containing the dataset that is considered to be the dependent variable
		"""
		if len(x_lst) != len(y_lst):
			raise ValueError(f"Length of x_lst 2 does not equal the length of y_lst {len(x_lst)}!={len(y_lst)}")
		if not isinstance(x_lst, StatList):
			self.x_lst = StatList(x_lst)
		else:
			self.x_lst = x_lst
		if not isinstance(y_lst, StatList):
			self.y_lst = StatList(y_lst)
		else:
			self.y_lst = y_lst
		self.standardDeviationSums = x_lst.standardDeviationSums(self.y_lst)
		self._r = self.standardDeviationSums / (self.x_lst.standard_deviation * (len(x_lst) - 1) * self.y_lst.standard_deviation)

	@staticmethod
	def strength(r: float) -> str:
		"""
		:param float r: The correlation coefficient of two data sets
		:return: The "strength" of the correlation coefficient
		:rtype: str
		"""
		r = abs(r)
		if r >= 0.8:
			return "STRONG"
		elif 0.4 <= r < 0.8:
			return "MEDIUM"
		elif 0 <= r < 0.4:
			return "WEAK"
		else:
			return "UNKNOWN STRENGTH"

	@staticmethod
	def positivity(r):
		"""
		:param float r: The correlation coefficient of two data sets
		:return: The positivity of the correlation coefficient
		:rtype: str
		"""
		return "POSITIVE" if r > 0 else "NEGATIVE"

	@property
	def r(self):
		"""
		:rtype: float
		:return: The correlation coefficient of the two data sets
		"""
		return self._r

	def __str__(self):
		"""
		:rtype: str
		:return: A string representation of the correlation coefficient
		"""
		return f"The R value is {self.r*100:.4}% which is a {self.strength(self.r)} {self.positivity(self.r)} value"

	def __len__(self):
		"""
		:rtype: int
		:return: The length of the data sets
		"""
		if len(self.x_lst) != len(self.y_lst):
			return len(self.x_lst)

	def __float__(self):
		return self.r

	@classmethod
	def create(cls):
		"""
		Finds the correlation coefficient of two data sets given by the user
		:rtype: :class: `stats.r.R`
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
		return cls(x_lst, y_lst)

	@property
	def x(self):
		"""
		:rtype: stats.StatList.StatList
		:return: The independent variable's StatList
		"""
		return self.x_lst

	@property
	def y(self):
		"""
		:rtype: stats.StatList.StatList
		:return: The dependent variable's StatList
		"""
		return self.y_lst
