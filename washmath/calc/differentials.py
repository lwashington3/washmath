from .. import Fraction
from ..classes.trig import E


def check_conditions(lst, ys, steps, until) -> bool:
	if steps is not None:
		return len(lst) < steps - 1
	return ys[-1] < until


def euler(h:float, x0, y0, function, n:int=None, until=None, answer_only=True) -> Fraction | tuple[tuple[Fraction], tuple[Fraction]]:
	"""
	:param float|int h: The horizontal step size
	:param int n: The number of steps to take
	:param int|float x0: The initial value of the independent variable
	:param int|float y0: The initial value of the dependent variable
	:param function: The function that is equivalent to the differential. Should take two arguments, the first being the independent variable, usually denoted as x, the second being the dependent variable, denoted as y
	:param bool answer_only: If the method should only return the final y, or the arrays of all answers
	"""
	if n is None and until is None:
		raise ValueError("Euler method needs number of steps (n) or until to define when the function is finished")

	xs = [Fraction(x0)]
	ys = [Fraction(y0)]
	indexes = [1]
	while check_conditions(indexes, ys, n, until):
		y = ys[-1] + (function(xs[-1], ys[-1]) * h)

		xs.append(xs[-1] + h)
		ys.append(y)
		indexes.append(indexes[-1] + 1)

	if answer_only:
		return ys[-1]

	return indexes, xs, ys


def P(t, p0, k, M) -> Fraction:
	"""
	:param int|float t: The amount of time that has passed
	:param int|float p0: The initial population
	:param int|float k:
	:param int|float M: The carrying capacity
	"""
	A = (M - p0) / p0
	denominator = 1 + (A * float(E(k*t)))
	return Fraction(M, denominator)
