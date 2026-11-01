import logging

import pytest

from inventory import apply_discount, calculate_total_price, check_stock


def test_calculate_total_price_valid():
    assert calculate_total_price(250.0, 4) == 1000.0


def test_calculate_total_price_zero_quantity():
    assert calculate_total_price(99.5, 0) == 0


@pytest.mark.parametrize(
    ("price", "quantity", "error"),
    [
        (-1, 2, ValueError),
        (10, -2, ValueError),
        ("10", 2, TypeError),
        (10, 2.5, TypeError),
        (True, 2, TypeError),
    ],
)
def test_calculate_total_price_invalid(price, quantity, error):
    with pytest.raises(error):
        calculate_total_price(price, quantity)


def test_apply_discount_valid():
    assert apply_discount(1000, 10) == 900


def test_apply_discount_boundaries():
    assert apply_discount(500, 0) == 500
    assert apply_discount(500, 100) == 0


@pytest.mark.parametrize(
    ("total", "discount", "error"),
    [
        (-100, 10, ValueError),
        (100, -5, ValueError),
        (100, 101, ValueError),
        ("100", 10, TypeError),
        (100, None, TypeError),
    ],
)
def test_apply_discount_invalid(total, discount, error):
    with pytest.raises(error):
        apply_discount(total, discount)


def test_check_stock_available():
    assert check_stock(10, 5) is True
    assert check_stock(5, 5) is True


def test_check_stock_insufficient():
    assert check_stock(3, 5) is False


@pytest.mark.parametrize(
    ("available", "requested", "error"),
    [
        (-1, 1, ValueError),
        (10, 0, ValueError),
        (10, -3, ValueError),
        (10.5, 1, TypeError),
        (10, "2", TypeError),
    ],
)
def test_check_stock_invalid(available, requested, error):
    with pytest.raises(error):
        check_stock(available, requested)


def test_logging_records_success(caplog):
    with caplog.at_level(logging.INFO):
        calculate_total_price(10, 2)
    assert "Total price calculated: 20" in caplog.text


def test_logging_records_error(caplog):
    with caplog.at_level(logging.ERROR), pytest.raises(ValueError):
        check_stock(10, 0)
    assert "Non-positive requested quantity" in caplog.text
