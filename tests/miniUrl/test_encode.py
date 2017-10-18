import pytest
from miniUrl.encode import encode, decode


@pytest.mark.parametrize("input, expected", [
    (0, 'x01'),
    (61779, 'Y4h'),
])
def test_encode(input, expected):
    assert encode(input) == expected


def test_encode_negative():
    with pytest.raises(ValueError):
        encode(-30)


@pytest.mark.parametrize("input, expected", [
    (0, 0),
    (61779, 61779),
])
def test_decode(input, expected):
    assert decode(encode(input)) == input


def test_decode_invalid_str():
    with pytest.raises(ValueError):
        decode('@AZQI-')