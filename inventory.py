"""Product inventory helpers with input validation and logging."""

import logging

logger = logging.getLogger(__name__)


def _is_number(value):
    """Return True for int/float values (bool is rejected on purpose)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_int(value):
    """Return True for int values (bool is rejected on purpose)."""
    return isinstance(value, int) and not isinstance(value, bool)


def calculate_total_price(price, quantity):
    """Return the total cost for `quantity` items priced at `price` each."""
    logger.info("Calculating total price: price=%s, quantity=%s", price, quantity)

    if not _is_number(price):
        logger.error("Invalid price type: %r", price)
        raise TypeError("price must be a number")
    if not _is_int(quantity):
        logger.error("Invalid quantity type: %r", quantity)
        raise TypeError("quantity must be an integer")
    if price < 0:
        logger.error("Negative price: %s", price)
        raise ValueError("price cannot be negative")
    if quantity < 0:
        logger.error("Negative quantity: %s", quantity)
        raise ValueError("quantity cannot be negative")

    total = price * quantity
    logger.info("Total price calculated: %s", total)
    return total


def apply_discount(total, discount_percent):
    """Return `total` after subtracting `discount_percent` percent."""
    logger.info("Applying discount: total=%s, discount=%s%%", total, discount_percent)

    if not _is_number(total) or not _is_number(discount_percent):
        logger.error("Non-numeric input: %r, %r", total, discount_percent)
        raise TypeError("total and discount_percent must be numbers")
    if total < 0:
        logger.error("Negative total: %s", total)
        raise ValueError("total cannot be negative")
    if not 0 <= discount_percent <= 100:
        logger.error("Discount out of range: %s", discount_percent)
        raise ValueError("discount_percent must be between 0 and 100")

    discounted = total - (total * discount_percent / 100)
    logger.info("Discounted amount: %s", discounted)
    return discounted


def check_stock(available_stock, requested_quantity):
    """Return True if `requested_quantity` can be fulfilled from stock."""
    logger.info(
        "Checking stock: available=%s, requested=%s",
        available_stock,
        requested_quantity,
    )

    if not _is_int(available_stock) or not _is_int(requested_quantity):
        logger.error("Non-integer stock input: %r, %r", available_stock, requested_quantity)
        raise TypeError("available_stock and requested_quantity must be integers")
    if available_stock < 0:
        logger.error("Negative available stock: %s", available_stock)
        raise ValueError("available_stock cannot be negative")
    if requested_quantity <= 0:
        logger.error("Non-positive requested quantity: %s", requested_quantity)
        raise ValueError("requested_quantity must be greater than zero")

    in_stock = requested_quantity <= available_stock
    if in_stock:
        logger.info("Stock check passed: request can be fulfilled")
    else:
        logger.warning("Stock check failed: insufficient stock")
    return in_stock


def main():
    """Small demo run that writes to the console and inventory.log."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler("inventory.log")],
    )

    total = calculate_total_price(499.99, 3)
    final = apply_discount(total, 10)
    available = check_stock(available_stock=5, requested_quantity=3)
    print(f"Total: {total:.2f} | After discount: {final:.2f} | In stock: {available}")

    try:
        check_stock(available_stock=5, requested_quantity=-1)
    except ValueError as error:
        print(f"Handled error: {error}")


if __name__ == "__main__":
    main()
