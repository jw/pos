from decimal import Decimal

from pytest import fixture

from pos.pos import LINE, PointOfSale

CATALOG: dict[str, Decimal] = {
    "12345": Decimal("10.0"),
    "54321": Decimal("0.1"),
    "11111": Decimal("0.2"),
    "22222": Decimal("100"),
}


@fixture
def pos():
    return PointOfSale(CATALOG)


def test_one_item(pos):
    pos.on_barcode("11111")
    assert f"{pos}" == "001: $0.2\n"


def test_no_item(pos):
    assert f"{pos}" == ""


def test_two_items(pos):
    pos.on_barcode("54321")
    pos.on_barcode("11111")
    assert f"{pos}" == "001: $0.1\n002: $0.2\n"


def test_one_item_total(pos):
    pos.on_barcode("11111")
    pos.on_total()
    assert f"{pos}" == f"001: $0.2\n{LINE}\nTOT: $0.2\n"


def test_no_item_total(pos):
    pos.on_total()
    assert f"{pos}" == f"{LINE}\nTOT: $0\n"


def test_two_items_total(pos):
    pos.on_barcode("54321")
    pos.on_barcode("11111")
    pos.on_total()
    assert f"{pos}" == f"001: $0.1\n002: $0.2\n{LINE}\nTOT: $0.3\n"
