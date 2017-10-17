import string

SYMBOLS = string.ascii_lowercase + string.ascii_uppercase + string.digits
SYMBOL_TO_DECIMAL_MAP = dict((symbol, decimal) for (decimal, symbol) in enumerate(SYMBOLS))
BASE = len(SYMBOLS)


# encodes number from base 10 to base BASE
# with least significant digit first
def encode(number):
    if number == 0:
        return SYMBOLS[0]
    encoded = []
    while number:
        print ("...")
        number, remainder = divmod(number, BASE)
        encoded.append(SYMBOLS[remainder])
    return ''.join(encoded)


# decodes number from base BASE to base 10
def decode(encoded):
    decoded = 0
    for digit_order, digit in enumerate(encoded):
        decoded += pow(BASE, digit_order)*SYMBOL_TO_DECIMAL_MAP[digit]
    return decoded


