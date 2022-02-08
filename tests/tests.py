import pos.pos
from pos.pos import Display


def test_first():
    display = Display()
    pos.pos.on_barcode(display, "12345")
    assert display.text == "$12.5"
        
