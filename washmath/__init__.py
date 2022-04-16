__author__ = "Len Washington III"
__version__ = "3.0.1"

from ._check_for_modules import warn_if_missing

for package in ["matplotlib", "numpy", "pandas"]:
    warn_if_missing(package)
del warn_if_missing

from .stats import *
from .calc import *
from .tools import *
from .fraction import Fraction
from .c_tools import factorial, factorial_without, gcd, P, C, sign
from .trig import PI, Trig, SIN, COS, TAN, ATAN