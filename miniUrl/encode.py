import string

SYMBOLS = string.ascii_lowercase + string.ascii_uppercase + string.digits
SYMBOL_TO_DECIMAL_MAP = dict((symbol, decimal) for (decimal, symbol) in enumerate(SYMBOLS))
BASE = len(SYMBOLS)


def encode(number):
    """
    given a positive integer (base 10) returns its representation in base 62
    with the least significant digit first
    :param number: integer
    :return: string
    """
    if number < 0:
        raise ValueError("only positive numbers supported")
    if number == 0:
        return SYMBOLS[0]
    encoded = []
    while number:
        number, remainder = divmod(number, BASE)
        encoded.append(SYMBOLS[remainder])
    return ''.join(encoded)


# decodes number from base BASE to base 10
def decode(encoded):
    """
    given a string representing the base62 representation of a positive integer,
    returns the base 10 integer
    :param encoded: string
    :return: integer
    """
    decoded = 0
    for digit_order, digit in enumerate(encoded):
        decoded += pow(BASE, digit_order)*SYMBOL_TO_DECIMAL_MAP[digit]
    return decoded


