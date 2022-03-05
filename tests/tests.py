from pytest import fixture

from pos.pos import PointOfSale

CATALOG: dict[str, float] = {
    "12345": 10.0,
    "54321": 0.1,
    "11111": 0.2,
    "22222": 100,
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
