from enum import Enum, auto


class Status(Enum):
    STARTED = auto()
    STOPPED = auto()


# This will be displayed when the item was not
# found or the barcode was invalid.
INVALID = "[INVALID]"


class PointOfSale:
    def __init__(self, catalog: dict[str, float]):
        self.catalog = catalog
        self.items = []
        self.status = Status.STARTED

    def on_barcode(self, barcode: str) -> None:
        self.items.append(self.catalog.get(barcode, None))

    def on_total(self, barcode: str) -> None:
        self.status = Status.STOPPED

    def __str__(self):
        """Shows
        001: $<price>
        002: $<price>
        -------------
        TOT: $<total>
        """
        result = ""
        total = 0.0
        for i, price in enumerate(self.items, start=1):
            if price:
                total += price
                price_as_str = f"${price}"
            else:
                price_as_str = INVALID
            result += f"{i:03}: {price_as_str}"
        if self.status == Status.STOPPED:
            result += "-------------"
            result += f"TOT: ${total}"
        return result
