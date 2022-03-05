from decimal import Decimal

from pytest import fixture

from pos.pos import LINE, PointOfSale

CATALOG: dict[str, Decimal] = {
    "12345": Decimal("10.0"),
    "54321": Decimal("0.1"),
    "11111": Decimal("0.2"),
    "22222": Decimal("100"),
}


CATALOG_WITH_EMPTY_AND_INVALID_ENTRIES: dict[str, Decimal] = {
    "11111": Decimal("1.11"),
    "22222": None,
    "33333": "invalid",
}


@fixture
def pos():
    return PointOfSale(CATALOG)


@fixture
def weird_pos():
    return PointOfSale(CATALOG_WITH_EMPTY_AND_INVALID_ENTRIES)


def test_one_item(pos):
    pos.on_barcode("11111")
    assert f"{pos}" == "001: $0.20\n"


def test_no_item(pos):
    assert f"{pos}" == ""


def test_two_items(pos):
    pos.on_barcode("54321")
    pos.on_barcode("11111")
    assert f"{pos}" == "001: $0.10\n002: $0.20\n"


def test_one_item_total(pos):
    pos.on_barcode("11111")
    pos.on_total()
    assert f"{pos}" == f"001: $0.20\n{LINE}\nTOT: $0.20\n"


def test_no_item_total(pos):
    pos.on_total()
    assert f"{pos}" == f"{LINE}\nTOT: $0.00\n"


def test_two_items_total(pos):
    pos.on_barcode("54321")
    pos.on_barcode("11111")
    pos.on_total()
    assert f"{pos}" == f"001: $0.10\n002: $0.20\n{LINE}\nTOT: $0.30\n"


def test_wrong_barcode(pos):
    pos.on_barcode("99999")
    assert f"{pos}" == "001: [INVALID]\n"
    pos.on_barcode("11111")
    assert f"{pos}" == "001: [INVALID]\n002: $0.20\n"
    pos.on_barcode("99999")
    pos.on_total()
    assert (
        f"{pos}" == f"001: [INVALID]\n002: $0.20\n003: [INVALID]\n{LINE}\nTOT: $0.20\n"
    )


def test_invalid_barcode(weird_pos):
    weird_pos.on_barcode("11111")
    weird_pos.on_barcode("22222")
    weird_pos.on_barcode("33333")
    assert f"{weird_pos}" == "001: $1.11\n002: [INVALID]\n003: [INVALID]\n"
    weird_pos.on_total()
    assert (
        f"{weird_pos}"
        == f"001: $1.11\n002: [INVALID]\n003: [INVALID]\n{LINE}\nTOT: $1.11\n"
    )


def test_manual_entry(weird_pos):
    weird_pos.on_manual(Decimal("0.50"))
    assert f"{weird_pos}" == "001: $0.50\n"


def test_manual_invalid_total_entry(weird_pos):
    weird_pos.on_manual(Decimal("0.50"))
    weird_pos.on_manual("invalid")
    assert f"{weird_pos}" == "001: $0.50\n002: [INVALID]\n"
    weird_pos.on_total()
    assert f"{weird_pos}" == f"001: $0.50\n002: [INVALID]\n{LINE}\nTOT: $0.50\n"


def test_manual_more_invalid_total_entry(weird_pos):
    weird_pos.on_manual(Decimal("0.50"))
    weird_pos.on_manual("invalid")
    weird_pos.on_barcode("333333")
    assert f"{weird_pos}" == "001: $0.50\n002: [INVALID]\n003: [INVALID]\n"
    weird_pos.on_total()
    assert (
        f"{weird_pos}"
        == f"001: $0.50\n002: [INVALID]\n003: [INVALID]\n{LINE}\nTOT: $0.50\n"
    )


def test_reset(pos):
    pos.on_manual(Decimal("0.50"))
    pos.on_reset()
    pos.on_manual(Decimal("1"))
    pos.on_barcode("12345")
    pos.on_total()
    assert f"{weird_pos}" f"001: $1.00\n002: $10.00\n{LINE}\nTOT: $11.00\n"


def test_multiple_resets_and_restart(pos):
    pos.on_reset()
    pos.on_reset()
    pos.on_reset()
    assert f"{weird_pos}" f""
    pos.on_total()
    assert f"{weird_pos}" f"{LINE}\nTOT: $0.00\n"
    pos.on_manual(Decimal("1.1111111"))
    assert f"{weird_pos}" f"001: $1.11\n"
    pos.on_barcode("11111")
    assert f"{weird_pos}" f"001: $1.11\n001: $0.20\n"
    pos.on_reset()
    assert f"{weird_pos}" f""


def test_total_onloy(pos):
    pos.on_total()
    assert f"{weird_pos}" f"{LINE}\nTOT: $0.00\n"
