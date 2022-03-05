from decimal import Decimal
from enum import Enum, auto

LINE = "-------------"


class Status(Enum):
    STARTED = auto()
    STOPPED = auto()


# This will be displayed when the item was not
# found or the barcode was invalid.
INVALID = "[INVALID]"


class PointOfSale:
    def __init__(self, catalog: dict[str, Decimal]):
        self.catalog = catalog
        self.items = []
        self.status = Status.STARTED

    def on_barcode(self, barcode: str) -> None:
        self.status = Status.STARTED
        self.items.append(self.catalog.get(barcode, None))

    def on_total(self) -> None:
        self.status = Status.STOPPED

    def __str__(self):
        """Shows
        001: $<price>
        002: $<price>
        -------------
        TOT: $<total>
        """
        result = ""
        total = Decimal(0)
        for i, price in enumerate(self.items, start=1):
            if price:
                total += price
                price_as_str = f"${price:.2f}"
            else:
                price_as_str = INVALID
            result += f"{i:03}: {price_as_str}\n"
        if self.status == Status.STOPPED:
            result += f"{LINE}\n"
            result += f"TOT: ${total:.2f}\n"
        return result
