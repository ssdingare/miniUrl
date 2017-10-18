import string
import re

SYMBOLS = string.digits + string.ascii_lowercase + string.ascii_uppercase
SYMBOL_TO_DECIMAL_MAP = dict((symbol, decimal) for (decimal, symbol) in enumerate(SYMBOLS))
BASE = len(SYMBOLS)
OFFSET = 3877
is_encoded = re.compile("[0-9a-zA-Z]+")


def encode(number):
    """
    given a positive integer (base 10) returns its representation in base BASE
    with the least significant digit first
    :param number: integer
    :return: string
    """
    if number < 0:
        raise ValueError("only positive numbers supported")
    number += OFFSET
    encoded = []
    while number:
        number, remainder = divmod(number, BASE)
        encoded.append(SYMBOLS[remainder])
    return ''.join(encoded)


# decodes number from base BASE to base 10
def decode(encoded):
    """
    given a string representing the base BASE representation of a positive integer,
    returns the base 10 integer
    :param encoded: string
    :return: integer
    """
    if not is_encoded.match(encoded):
        raise ValueError("Not a base{0!s} representation".format(BASE))
    decoded = 0
    for digit_order, digit in enumerate(encoded):
        decoded += pow(BASE, digit_order)*SYMBOL_TO_DECIMAL_MAP[digit]
    return decoded - OFFSET


