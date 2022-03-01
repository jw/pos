from pytest import fixture

from pos.pos import INVALID, Display


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
