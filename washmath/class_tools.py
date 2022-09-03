def is_numeric(obj):
	from .classes import Fraction
	from numpy import int32, int64
	return isinstance(obj, (int, float, Fraction, int32, int64))
