from abc import abstractmethod
from enum import Enum, auto
from typing import Protocol

STORE: dict[str, float] = {
    "12345": 12.5,
    "33333": 33.33,
    "44444": 44.44,
}


class Status(Enum):
    VALID = auto()
    INVALID = auto()


# This will be displayed when the item was not
# found or the barcode was invalid.
INVALID = "[INVALID]"


class PointOfSale(Protocol):
    @abstractmethod
    def on_barcode(self, barcode: str) -> None:
        raise NotImplementedError  # pragma: no cover


class Display(PointOfSale):
    def __init__(self):
        self._status = Status.VALID
        self._price = 0

    @property
    def price(self) -> int:
        return self._price

    @price.setter
    def price(self, price: int) -> None:
        if price is None or not isinstance(price, int | float):
            self._price = -1
            self._status = Status.INVALID
        else:
            self._price = price
            self._status = Status.VALID

    def __str__(self) -> str:
        """
        When a valid price was given, show [$<price>]
        otherwise show `INVALID`.
        """
        if self._status is Status.INVALID:
            return INVALID
        else:
            return f"[${self._price}]"

    def on_barcode(self, barcode: str) -> None:
        self.price = STORE.get(barcode, None)
