from decimal import Decimal

from cart.pricing import LineItem, Discount, price_cart, apply_discounts
from cart.checkout import quote, amount_due_cents


def money(s):
    return Decimal(s)


def test_subtotal_and_tax_no_discount():
    items = [LineItem("A", 2, money("10.00")), LineItem("B", 1, money("30.00"))]
    b = price_cart(items, tax_rate=money("0.08"))
    assert b.subtotal == money("50.00")
    assert b.taxable_base == money("50.00")
    assert b.tax == money("4.00")
    assert b.shipping == money("0")
    assert b.total == money("54.00")


def test_non_stackable_picks_best():
    d1 = Discount("TEN", percent=money("10"))
    d2 = Discount("FIVEOFF", flat=money("5.00"))
    total, applied = apply_discounts(money("100.00"), [d1, d2])
    assert total == money("10.00")
    assert applied == ["TEN"]


def test_stackable_adds_on_top():
    d1 = Discount("TEN", percent=money("10"))
    d2 = Discount("SHIP2", flat=money("2.00"), stackable=True)
    total, applied = apply_discounts(money("100.00"), [d1, d2])
    assert total == money("12.00")
    assert sorted(applied) == ["SHIP2", "TEN"]


def test_min_subtotal_gate():
    d = Discount("BIG", percent=money("50"), min_subtotal=money("100"))
    total, applied = apply_discounts(money("99.99"), [d])
    assert total == money("0")
    assert applied == []


def test_mixed_taxable_with_discount_prorates():
    """A discount on a cart with a non-taxable item must only reduce the
    taxable base by the taxable share of the discount."""
    items = [
        LineItem("TAXED", 1, money("50.00"), taxable=True),
        LineItem("GIFTCARD", 1, money("50.00"), taxable=False),
    ]
    d = Discount("TEN", percent=money("10"))  # $10 off a $100 cart
    b = price_cart(items, [d], tax_rate=money("0.08"))
    assert b.subtotal == money("100.00")
    assert b.discount_total == money("10.00")
    # taxable share = 50/100 -> $5 of the discount hits the taxable base
    assert b.taxable_base == money("45.00")
    assert b.tax == money("3.60")
    assert b.total == money("93.60")


def test_all_nontaxable_cart_has_no_tax():
    items = [LineItem("GC", 2, money("40.00"), taxable=False)]
    d = Discount("TEN", percent=money("10"))
    b = price_cart(items, [d], tax_rate=money("0.08"))
    assert b.taxable_base == money("0")
    assert b.tax == money("0")


def test_checkout_quote_shape():
    items = [LineItem("A", 1, money("60.00"))]
    q = quote(items)
    assert q["total"] == "64.80"
    assert amount_due_cents(items) == 6480
