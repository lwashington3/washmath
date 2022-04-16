from sys import argv
from re import search as match
from .statlist import StatList
from ..fraction import Fraction


if __name__ == "__main__":
    if len(argv) > 1:
        lst = []
        for arg in argv[1:]: #4/5
            check = match("([0-9]+.?[0-9]?)\\s?/\\s?([0-9]+.?[0-9]?)", arg)
            if check is not None:
                numerator = float(check.group(1))
                denominator = float(check.group(2))
                lst.append(Fraction(numerator, denominator))
            else:
                lst.append(float(arg))
        print(StatList(lst).dataSummary())
