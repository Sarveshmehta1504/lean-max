"""Checkout orchestration — caller of the pricing engine."""
from decimal import Decimal

from .pricing import LineItem, Discount, price_cart


TAX_RATE = Decimal("0.08")


def quote(items, discounts=()):
    b = price_cart(items, discounts, tax_rate=TAX_RATE)
    return {
        "subtotal": str(b.subtotal),
        "discount": str(b.discount_total),
        "tax": str(b.tax),
        "shipping": str(b.shipping),
        "total": str(b.total),
        "codes": b.applied,
    }


def amount_due_cents(items, discounts=()) -> int:
    b = price_cart(items, discounts, tax_rate=TAX_RATE)
    return int(b.total * 100)
