from __future__ import absolute_import

__author__ = "Len Washington III"
__version__ = "3.0.0"
# Statistical Analysis List


from ..tools import *
from ..classes import Fraction
try:
	from matplotlib import pyplot as plt
	import numpy as np
except ModuleNotFoundError:
	print("Numpy or Matplotlib not installed. Cannot run plot functions")
except ImportError:
	print("Numpy or Matplotlib not installed. Cannot run plot functions")


class StatList(list):
	"""
	A class used to help with statistical analysis of a list of data. Used in almost all classes in this package. Most functions do not rely on outside packages
	"""

	def __init__(self, *values, title="", allow_fractions=True):
		"""
		:param list lst: The collection of elements that you want to analyze
		:param str title: A title or name you want to give the data set
		:param boolean allow_fraction: Whether the list will be allowed to hold Fraction objects
		"""
		super().__init__([None] * len(values))
		self.allow_fractions = allow_fractions
		for i, value in enumerate(values):
			self[i] = Fraction(value)
		self._containing_fractions = self._check_if_containing_fractions()
		self.title = title
		self.calculate_attributes()

	def __str__(self) -> str:
		"""
		The string of the class contains all the data in the class, as well as the title if it is set
		:return: The string of the class
		"""
		if self.title == "":
			return f"Statistical list of {super().__str__()}"
		else:
			return f"Statistical list of {self.title}: {super().__str__()}"

	def __eq__(self, other):
		if isinstance(other, (StatList, list, tuple)):
			if len(self) != len(other):
				return False
			for x, y in zip(self, other):
				if x != y:
					return False
			return True
		elif hasattr(other, "__iter__"):
			return super() == list(other)
		else:
			return False

	def __hash__(self):
		return hash(([i for i in self], self.title))

	def __add__(self, other):
		"""
		:param other: A StatList, list, or tuple
		:return: Another StatList containing both the list of this StatList and the given data
		:raise: TypeError if other is not of type StatList, list, or tuple
		"""
		if isinstance(other, StatList):
			return StatList(self.getList() + other.getList())
		elif isinstance(other, (list, tuple)):
			lst = self.getList()
			lst.extend(other)
			return StatList(lst)
		elif is_numeric(other):
			return StatList(self.getList() + [other])
		else:
			raise TypeError(f"unsupported operand type(s) for +: 'StatList' and 'f{type(other).__name__}'")

	def __sub__(self, other):
		"""
		:param other: A StatList, list, or tuple
		:return: Another StatList containing both the list of this StatList and the given data
		:raise: TypeError if other is not of type StatList, list, or tuple
		"""
		if isinstance(other, (StatList, list, tuple)):
			lst = list(other).copy()
			for i in other:
				try:
					lst.remove(i)
				except ValueError:
					print(f"{i} is not in the original list")
			return StatList(lst)
		elif is_numeric(other):
			lst = self.getList()
			lst.remove(other)
			return StatList(lst)
		else:
			raise TypeError(f"unsupported operand type(s) for -: 'StatList' and 'f{type(other).__name__}'")

	def __mul__(self, other):
		"""
		:param other: A StatList, list, or tuple
		:return: Another StatList containing both the list of this StatList and the given data
		:raise: TypeError if other is not of type StatList, list, or tuple
		"""
		if isinstance(other, (StatList, list, tuple)):
			if len(other) == len(self):
				lst = [x * y for (x, y) in zip(self, other)]
				return StatList(lst)
			else:
				raise ValueError(f"The length of the given StatList does not match the length of the original StatList")
		elif is_numeric(other):
			return StatList([i * other for i in self])
		else:
			raise TypeError(f"unsupported operand type(s) for *: 'StatList' and 'f{type(other).__name__}'")

	def __truediv__(self, other):
		"""
		:param other: A StatList, list, or tuple
		:return: Another StatList containing both the list of this StatList and the given data
		:raise: TypeError if other is not of type StatList, list, or tuple
		"""
		if isinstance(other, (StatList, list, tuple)):
			if len(other) == len(self):
				lst = [x / y for (x, y) in zip(self, other)]
				return StatList(lst)
			else:
				raise ValueError(f"The length of the given iterative does not match the length of the original StatList")
		elif is_numeric(other):
			return StatList([i / other for i in self])
		else:
			raise TypeError(f"unsupported operand type(s) for /: 'StatList' and 'f{type(other).__name__}'")

	def __floordiv__(self, other):
		"""
		:param other: A StatList, list, or tuple
		:return: Another StatList containing both the list of this StatList and the given data
		:raise: TypeError if other is not of type StatList, list, or tuple
		"""
		if hasattr(other, "__iter__"):
			if len(other) != len(self):
				raise ValueError(f"The length of the given StatList does not match the length of the original StatList")
			lst = [x // y for (x, y) in zip(self, other)]
			return StatList(lst)
		elif is_numeric(other):
			return StatList([i // other for i in self])
		else:
			raise TypeError(f"unsupported operand type(s) for //: 'StatList' and 'f{type(other).__name__}'")

	def __mod__(self, other):
		"""
		:param other: A StatList, list, or tuple
		:return: Another StatList containing both the list of this StatList and the given data
		:raise: TypeError if other is not of type StatList, list, or tuple
		"""
		if isinstance(other, (StatList, list, tuple)):
			if len(other) == len(self):
				lst = [x % y for (x, y) in zip(self, other)]
				return StatList(lst)
			else:
				raise ValueError(f"The length of the given StatList does not match the length of the original StatList")
		elif is_numeric(other):
			return StatList([i % other for i in self])
		else:
			raise TypeError(f"unsupported operand type(s) for %: 'StatList' and 'f{other.__name__}'")

	def __pow__(self, other):
		"""
		:param other: A StatList, list, or tuple
		:return: Another StatList containing both the list of this StatList and the given data
		:raise: TypeError if other is not of type StatList, list, or tuple
		"""
		if isinstance(other, (StatList, list, tuple)):
			if len(other) == len(self):
				lst = [x ** y for (x, y) in zip(self, other)]
				return StatList(lst)
			else:
				raise ValueError(f"The length of the given iterative does not match the length of the original StatList")
		elif is_numeric(other):
			return StatList([i ** other for i in self])
		else:
			raise TypeError(f"unsupported operand type(s) for /: 'StatList' and 'f{other.__name__}'")

	def __iadd__(self, other) -> None:
		"""
		The StatList class is meant to be immutable. If you want a StatList with added elements, use the '+' method to create another object
		:raise ValueError:
		"""
		raise ValueError(
			f"The StatList class is meant to be immutable. If you want a StatList with added elements, use the '+' method to create another object")

	def __isub__(self, other) -> None:
		"""
		The StatList class is meant to be immutable. If you want a StatList with subtracted elements, use the '-' method to create another object
		:raise ValueError:
		"""
		raise ValueError(
			f"The StatList class is meant to be immutable. If you want a StatList with subtracted elements, use the '-' method to create another object")

	def __imul__(self, other) -> None:
		"""
		The StatList class is meant to be immutable. If you want a StatList with multiplied elements, use the '*' method to create another object
		:raise ValueError:
		"""
		raise ValueError(
			f"The StatList class is meant to be immutable. If you want a StatList with multiplied elements, use the '*' method to create another object")

	def __idiv__(self, other) -> None:
		"""
		The StatList class is meant to be immutable. If you want a StatList with divided elements, use the '/' method to create another object
		:raise ValueError:
		"""
		raise ValueError(
			f"The StatList class is meant to be immutable. If you want a StatList with divided elements, use the '/' method to create another object")

	def __ifloordiv__(self, other) -> None:
		"""
		The StatList class is meant to be immutable. If you want a StatList with floor-divided elements, use the '//' method to create another object
		:raise ValueError:
		"""
		raise ValueError(
			f"The StatList class is meant to be immutable. If you want a StatList with floor-divided elements, use the '//' method to create another object")

	def __imod__(self, other) -> None:
		"""
		The StatList class is meant to be immutable. If you want a StatList with modulated elements, use the '%' method to create another object
		:raise ValueError:
		"""
		raise ValueError(
			f"The StatList class is meant to be immutable. If you want a StatList with modulated elements, use the '%' method to create another object")

	def __ipow__(self, other) -> None:
		"""
		The StatList class is meant to be immutable. If you want a StatList with powered elements, use the '**' method to create another object
		:raise ValueError:
		"""
		raise ValueError(
			f"The StatList class is meant to be immutable. If you want a StatList with powered elements, use the '+' method to create another object")

	@property
	def title(self) -> str:
		"""
		:type: str
		:return: The title of the data set if it was set
		"""
		return self._title

	@title.setter
	def title(self, title: str) -> None:
		"""
		Sets the title of the data set
		:param str title: The title
		"""
		self._title = str(title)

	def getList(self) -> list:
		"""
		:rtype: :list: The data in a list
		:return: The collection of data being used
		"""
		return super().copy()

	def __setitem__(self, key, value):
		if not self.allow_fractions:
			if isinstance(value, object):
				__value = float(value)
		super().__setitem__(key, value)

	def _check_if_containing_fractions(self) -> bool:
		self._containing_fractions = any([isinstance(i, Fraction) for i in self])
		return self.containing_fractions

	@property
	def containing_fractions(self):
		return self._containing_fractions

	def append(self, __object) -> None:
		if not self.allow_fractions:
			if isinstance(__object, Fraction):
				__object = float(Fraction)
		super().append(__object)
		self._containing_fractions = self._check_if_containing_fractions()
		self.calculate_attributes()

	def clear(self) -> None:
		super().clear()
		self._containing_fractions = self._check_if_containing_fractions()
		self.calculate_attributes()

	# TODO: Add fraction checking for extension methods
	def extend(self, __iterable) -> None:
		super().extend(__iterable)
		self._containing_fractions = self._check_if_containing_fractions()
		self.calculate_attributes()

	def insert(self, __index: int, __object) -> None:
		if not self.allow_fractions:
			if isinstance(__object, Fraction):
				__object = float(Fraction)
		super().insert(__index, __object)
		self._containing_fractions = self._check_if_containing_fractions()
		self.calculate_attributes()

	def pop(self, __index: int = ...):
		value = super().pop(__index)
		self._containing_fractions = self._check_if_containing_fractions()
		self.calculate_attributes()
		return value

	def remove(self, __value) -> None:
		super().remove(__value)
		self._containing_fractions = self._check_if_containing_fractions()
		self.calculate_attributes()

	def reverse(self) -> None:
		super().remove()
		self._containing_fractions = self._check_if_containing_fractions()
		self.calculate_attributes()

	def sort(self, *, key=lambda value: float(value), reverse: bool = ...) -> None:
		"""if self.allow_fractions:
			if key is None:
				key = lambda value: float(value)"""
		super().sort(key, reverse)
		self._containing_fractions = self._check_if_containing_fractions()
		self.calculate_attributes()

	def calculate_attributes(self) -> None:
		self._setSum()
		self._setMean()
		self._setMode()
		self._setMin()
		self._setMax()
		self._median = removeDecimal(self._getMedian(self.copy()))
		self._setStandardDeviation()
		self._setQ1()
		self._setQ3()
		self._setRange()
		self._setIQR()
		self._setOutlierRange()
		self._setOutliers()
		self._setAverageDeviation()
		self._setVariance()
		self._setStandardError()

	def _setSum(self):
		self._sum = sum(self, start=Fraction(0))

	def _setMean(self):
		self._mean = Fraction(self.sum, len(self))

	def _setMode(self):
		mode = None
		times = 0

		try:
			for unique_value in set(self):
				count = super().count(unique_value)
				if count > times:
					mode = unique_value
					times = count
		except np.core._exceptions.UFuncTypeError as e:
			from warnings import warn
			warn(f"The most could not be calculated due to: {e}")

		self._mode = mode

	def _setMin(self):
		copy = self.copy()
		copy.sort()
		self._min = copy[0]

	def _setMax(self):
		lst = self.copy()
		lst.sort()
		self._max = lst[-1]

	@staticmethod
	def _getMedian(lst) -> float:
		lst.sort()
		if len(lst) % 2 == 0:
			value1 = lst[len(lst) // 2]
			value2 = lst[len(lst) // 2 - 1]

			if not any([isinstance(i, Fraction) for i in lst]):
				return (value1 + value2) / 2

			if not isinstance(value1, Fraction):
				return (value2 + value1) / 2  # Need to make sure the right adder is called
			return (value1 + value2) / 2
		else:
			return lst[(len(lst) // 2)]

	def _setStandardDeviation(self):
		if len(self) == 1:
			self._standardDeviation = 0
			return
		squares = [(Fraction(point) - self.mean) ** 2 for point in self]
		self._standardDeviation = sum(squares, start=Fraction(0, 1))
		self._standardDeviation /= (len(self) - 1)  # I have len(self) - 1 but some sources say just len(self), including Google Sheets, look into which is right
		self._standardDeviation **= 0.5

	def _setQ1(self):
		lst = self.getList()
		lst.sort()
		if len(lst) % 2 == 1:
			lst = lst[:int(len(lst) / 2)]
		else:
			lst = lst[:(len(lst) // 2)]
		self._Q1 = self._getMedian(lst)

	def _setQ3(self):
		lst = self.getList()
		lst.sort()
		if len(lst) % 2 == 1:
			lst = lst[int(len(lst) / 2) + 1:]
		else:
			lst = lst[(len(lst) // 2):]
		self._Q3 = self._getMedian(lst)

	def _setRange(self):
		self._range = self.max - self.min

	def _setIQR(self):
		self._IQR = self.Q3 - self.Q1

	def _setOutlierRange(self):
		outlier = Fraction(3, 2) * self.IQR
		self._outlier_range = (outlier - self.Q1, outlier + self.Q3)

	def _setOutliers(self):
		self._outliers = tuple(point for point in self if self.isOutlier(point))

	def _setAverageDeviation(self):
		lst = [abs(-self.mean + point) for point in self]
		self._averageDeviation = Fraction(sum(lst, start=Fraction(0, 1)), len(self))

	def _setVariance(self):
		lst = [(-self.mean + point) ** 2 for point in self]
		self._variance = sum(lst, start=Fraction(0,1)) / (len(self) - 1)

	def _setStandardError(self):
		self._standardError = Fraction(self.standard_deviation, np.sqrt(len(self)))

	@property
	def sum(self) -> int:
		"""
		:rtype: :float:
		:return: The sum of all the data in the collection
		"""
		return self._sum

	@property
	def mean(self):
		"""
		:rtype: :float:
		:return: The average/mean of all the data in the collection
		"""
		return self._mean

	@property
	def average(self):
		"""
		:rtype: :float:
		:return: The average/mean of all the data in the collection
		"""
		return self.mean

	@property
	def mode(self):
		"""
		:rtype: float
		:return: The most common data point in a collection
		"""
		return self._mode

	@property
	def min(self):
		"""
		:rtype: float or int
		:return: The minimum data point in the collection
		"""
		return self._min

	@property
	def max(self):
		"""
		:rtype: float or int
		:return: The maximum data point in the collection
		"""
		return self._max

	@property
	def median(self) -> int:
		"""
		:rtype: int or float
		:return: The middle point of the collection
		"""
		return self._median

	@property
	def standard_deviation(self):
		"""
		:rtype: float
		:return: The standard deviation of the collection
		"""
		return self._standardDeviation

	@property
	def Q1(self):
		"""
		:return: The 1st Quartile in the data collection
		"""
		return self._Q1

	@property
	def Q3(self):
		"""
		:return: The third quartile in the data set
		"""
		return self._Q3

	@property
	def range(self):
		"""
		:return: The range of the data set
		"""
		return self._range

	@property
	def IQR(self):
		"""
		:return: The interquartile range of the collection
		"""
		return self._IQR

	@property
	def outlier_range(self):
		"""
		Returns a tuple of the outliers. If a point is less than the first value or greater than the second value, it is an outlier
		:rtype: tuple
		:return: The points that would be considered outliers in the data set
		"""
		return self._outlier_range

	@property
	def outliers(self):
		"""
		:rtype: tuple
		:return: All the outliers in the dataset
		"""
		return self._outliers

	@property
	def average_deviation(self):
		"""
		Returns the average deviation, also known as mean absolute deviation.
		:return: The average deviation
		"""
		return self._averageDeviation

	@property
	def variance(self):
		return self._variance

	@property
	def standard_error(self):
		"""
		Returns the standard, calculated using the standard deviation / sqrt(number of elements)
		:return: The average deviation
		"""
		return self._standardError

	def covariance(self, other) -> Fraction:
		"""
		:param StatList other:
		"""
		if not isinstance(other, StatList):
			raise ValueError(f"The other variable must be a Statlist, not {type(other).__name__}")
		if len(self) != len(other):
			raise ValueError(f"The statlists must be the same length. {len(self)} !+ {len(other)}")
		value = Fraction(0)
		for x1, x2 in zip(self, other):
			value += Fraction(x1 - self.mean) * Fraction(x2 - other.mean)
		return value / len(self)

	def isOutlier(self, point) -> bool:
		"""
		:param float point: The point you want to check to see if it is an outlier
		:rtype: boolean
		:return: If the given point is an outlier
		"""
		return self.outlier_range[0] > point or self.outlier_range[1] < point

	def dataSummary(self, tab=True, vertical=True) -> str:
		"""Gives a brief summary of values in this project
		:param boolean tab: Return the data in an organized table format if True. False returns a list of lists
		:param boolean vertical: Defines the orientation of the table. Default is vertical.
		:return: Data in a table format
		"""
		data = [
			["Statistics", self.title],
			["Length", len(self)],
			["Sum", self.sum],
			["Minimum", self.min],
			["Q1", self.Q1],
			["Median", self.median],
			["Q3", self.Q3],
			["Maximum", self.max],
			["Mean", self.mean],
			["Mode", self.mode],
			["Range", self.range],
			["InterQuartile Range", self.IQR],
			["Outlier Range", self.outlier_range],
			["Number of Outliers", len(self.outliers)],
			["Variance", self.variance],
			["Standard Deviation", self.standard_deviation],
			["Average Deviation", self.average_deviation]
		]
		if not vertical:
			data = [[i[0][x] for i in zip(data)] for x in range(len(data[0]))]
		if tab:
			from tabulate import tabulate
			data = tabulate(data)
		return data

	def standardDeviationSums(self, other) -> Fraction:
		"""
		Returns the sum of each standard deviation in lst1 and lst2. Used for calculating the correlation coefficient.
		:param stats.StatList.StatList other:
		:return: The sum of standard deviations
		"""
		if len(self) != len(other):
			raise ValueError(f"Length of lst1 does not equal the length of lst2: {len(self)}!={len(other)}")
		elif not isinstance(other, StatList):
			raise TypeError(f"other is not of type 'StatList'\nAdd StatList() around the parameter you pass")
		summation = Fraction(0)
		for x, y in zip(self, other):
			x_diff = Fraction(x) - self.mean
			y_diff = Fraction(y) - other.mean
			summation += (x_diff * y_diff)
		return summation

	@classmethod
	def create(cls):
		"""
		Creates a StatList from the user inputting data
		:return: A StatList of the data given
		:rtype: :class: `stats.StatList.StatList`
		"""
		lst = []
		while True:
			element = input("Input the next element in the list. Enter nothing to finish. ")
			if not element:
				break
			lst.append(float(element))
		return cls(lst)

	@staticmethod
	def sortMultipleLists(sort, dependent):
		"""
		Sorts two StatLists so the index matches when one is sorted
		:param stats.StatList.StatList sort: The list that is getting sorted
		:param stats.StatList.StatList dependent: The list that will get sorted based off of the other list
		:returns: The StatLists, one sorted and the other matching the changed indexes
		:rtype: (stats.StatList.StatList, stats.StatList.StatList)
		"""
		new_x, new_y = [], []
		for (x, y) in zip(sort, dependent):
			new_x.append(x)
			new_x.sort()
			new_y.insert(new_x.index(x), y)
		return StatList(new_x), StatList(new_y)

	@staticmethod
	def fromCsv(path: str, delimiter=",") -> tuple:
		"""
		Returns a number of StatLists from a csv file. Works for tsv is the delimiter is set.
		:param str path: The path to the file
		:param str delimiter: The delimiter of the file. Default is ',' for comma-separated values (csv)
		:return: A tuple of StatList
		"""
		data = open(path).readlines()
		if not len(data):
			return
		for line in data:
			length = len(line.split(delimiter))
		hold = [[] for _ in range(length)]
		for line in data:
			tmp = line.split(delimiter)
			tmp = [i.strip().replace("\n", "") for i in tmp]
			for i in range(len(tmp)):
				try:
					hold[i].append(Fraction(float(tmp[i])))
				except ValueError:
					hold[i].append(tmp[i])
		final = []
		for i in hold:
			title = i.pop(0)
			if not isinstance(title, str):
				i.insert(title, 0)
				title = ""
			final.append(StatList(*i, title=title))
		return tuple(final)
