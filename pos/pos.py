STORE = {
    "12345": "$12.5",
    "33333": "$33.33",
    "44444": "$44.44",
}

INVALID = "[INVALID]"


class Display:

    def __init__(self):
        self.text = ""

    def set_text(self, price: str):
        self.text = price

    def __str__(self):
        print(f"[{self.text}]")


def on_barcode(display: Display, barcode: str):
    if barcode in STORE:
        display.set_text(STORE[barcode])
    else:
        display.set_text(INVALID)
