from ..tools import Fraction


def euler(h:float, n:int, x0, y0, func, answer_only=True) -> Fraction | tuple[tuple[Fraction], tuple[Fraction]]:
	"""
	:param float|int h: The horizontal step size
	:param int n: The number of steps to take
	:param int|float x0: The initial value of x
	:param int|float y0: The initial value of y
	:param function func: The function that is equivalent to the differential. Should take two arguments, the first being the independent variable, usually denoted as x, the second being the dependent variable, denoted as y
	:param bool answer_only: If the method should only return the final y, or the arrays of all answers
	"""
	xs = [Fraction(x0)]
	ys = [Fraction(y0)]
	for i in range(1, n):
		xs.append(xs[-1] + h)
		ys.append(ys[-1] + (func(xs[-1], ys[-1]) * h))
	if answer_only:
		return ys[-1]
	return xs, ys