from .fraction import Fraction, is_numeric
from re import sub


def removeDecimal(value: float) -> int | Fraction:
    """
    Removes an unnecessary decimal for a better look
    :param float value: Value you want to check
    :return: The value in integer for if it is an int
    """
    if isinstance(value, Fraction):
        return value
    int_val = int(value)
    return int_val if value == int_val else value


def superscript(string:str) -> str:
    """
    Takes a string that contains ^ and turns the numbers that follow into exponents for matplotlib
    :param str string: The raw string containing "^"
    :return: The formatted string
    """  # FIXME: If there are multiple carats in the expression
    return sub(r"(.*)?(\(?)(.+)\^([0-9.]+)(\)?)", r"\1\2$\3^{\4}$\5", string)


def subscript(string:str) -> str:
    """
    Takes a string that contains '_' and turns the sequence that follow into exponents for matplotlib
    :param str string: The raw string containing "_"
    :return: The formatted string
    """
    return sub(r"(.*)?(\(?)(.+)_([0-9.]+)(\)?)", r"\1\2$\3_{\4}$\5", string)
