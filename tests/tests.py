from pytest import fixture

import pos.pos
from pos.pos import Display


@fixture
def display():
    return Display()


def test_first(display):
    pos.pos.on_barcode(display, "12345")
    assert display.text == "$12.5"


def test_nothing(display):
    pos.pos.on_barcode(display, "")
    assert display.text == pos.pos.INVALID


def test_invalid(display):
    pos.pos.on_barcode(display, "000000")
    assert display.text == pos.pos.INVALID
