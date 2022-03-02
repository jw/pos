from pytest import fixture

from pos.pos import INVALID, Display, PointOfSale


@fixture
def display():
    return Display()


def test_first(display):
    display.on_barcode("12345")
    assert f"{display}" == "[$12.5]"


def test_nothing(display):
    display.on_barcode("")
    assert f"{display}" == INVALID


def test_invalid(display):
    display.on_barcode("000000")
    assert f"{display}" == INVALID


def test_none(display):
    display.on_barcode(None)
    assert f"{display}" == INVALID


def test_display_setter(display):
    display.price = "forty-two"
    assert f"{display}" == INVALID
    display.price = None
    assert f"{display}" == INVALID

    display.price = 42
    assert f"{display}" == "[$42]"
    display.price = 4.2
    assert f"{display}" == "[$4.2]"


def test_display_getter(display):
    assert display.price == 0
    display.price = 100
    assert display.price == 100
    display.price = "invalid"
    assert display.price == -1
