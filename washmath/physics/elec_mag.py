from ..classes import Fraction


def total_series_capacity(*capacities) -> Fraction:
	capacity = Fraction(0, 1)

	for cap in capacities:
		capacity += Fraction(1, cap)

	return Fraction(capacity.denominator, capacity.numerator)


def total_parallel_capacity(*capacities) -> Fraction:
	capacity = Fraction(0, 1)

	for cap in capacities:
		capacity += Fraction(cap)

	return capacity
