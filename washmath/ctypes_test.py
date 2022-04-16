import ctypes
import pathlib


if __name__ == "__main__":
    libname = pathlib.Path("/mnt/d/Users/balence/Desktop/Programming/C++/washmath/build/libwashmath.so")
    c_lib = ctypes.CDLL(libname)
    print(dir(c_lib))
    print(c_lib.Fraction(1, 2)+1)