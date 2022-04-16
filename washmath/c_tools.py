from ctypes import CDLL, c_long, c_int, c_float, c_ulonglong
from ctypes.util import find_library
from pathlib import Path
from os.path import dirname, realpath


path = find_library(f"{dirname(realpath(__file__))}/c_libs/washmath")
if path is None:
    path = f"{dirname(realpath(__file__))}/c_libs/libwashmath.so"
_c_lib = CDLL(path)
_c_lib.factorial.restype = c_ulonglong
_c_lib.gcd.restype = c_long
_c_lib.P.restype = c_ulonglong
_c_lib.C.restype = c_ulonglong
_c_lib.sign.restype = c_int


def sign(n:int) -> c_int:
    return _c_lib.sign(c_int(n))


def factorial(n:int) -> c_ulonglong|int:
    if n <= 20:
        return _c_lib.factorial(c_int(n))
    total = 1
    for i in range(1, n+1):
        total *= i
    return total


def factorial_without(n:int, r:int) -> int:
    """
    Calculates the factorial for n, exclusing all elements less than or equal to (inclusive) r
    :param n: The main integer to be factorialized
    :type n:
    :param r:
    :type r:
    :return:
    :rtype:
    """
    total = 1
    for i in range(r+1, n+1):
        total *= i
    return total

# TODO: Continue writing test cases
def gcd(a:int, b:int) -> c_ulonglong:
    return _c_lib.gcd(c_long(a), c_long(b))


def P(a:int, b:int) -> c_int:
    return _c_lib.P(c_int(a), c_int(b))


def C(a:int, b:int) -> c_int:
    return _c_lib.C(c_int(a), c_int(b))

"""
def gcd(a, b):
    if a == 0 or b == 0:
        return 0;
    elif a == b:
        return a
    elif abs(a) == 1 or abs(b) == 1:
        return 1
    elif a > b:
        return gcd(a-b, b)
    return gcd(a, b-a)"""