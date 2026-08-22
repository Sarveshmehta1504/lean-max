"""Pricing engine for the cart service."""
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable, Optional

CENTS = Decimal("0.01")


@dataclass(frozen=True)
class LineItem:
    sku: str
    qty: int
    unit_price: Decimal
    taxable: bool = True


@dataclass(frozen=True)
class Discount:
    code: str
    percent: Decimal = Decimal("0")
    flat: Decimal = Decimal("0")
    min_subtotal: Decimal = Decimal("0")
    stackable: bool = False


@dataclass
class PriceBreakdown:
    subtotal: Decimal = Decimal("0")
    discount_total: Decimal = Decimal("0")
    taxable_base: Decimal = Decimal("0")
    tax: Decimal = Decimal("0")
    shipping: Decimal = Decimal("0")
    total: Decimal = Decimal("0")
    applied: list = field(default_factory=list)


def _round(value: Decimal) -> Decimal:
    return value.quantize(CENTS, rounding=ROUND_HALF_UP)


def line_total(item: LineItem) -> Decimal:
    return _round(item.unit_price * item.qty)


def subtotal_of(items: Iterable[LineItem]) -> Decimal:
    return _round(sum((line_total(i) for i in items), Decimal("0")))


def taxable_subtotal(items: Iterable[LineItem]) -> Decimal:
    return _round(sum((line_total(i) for i in items if i.taxable), Decimal("0")))


def _helper_rule_01(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 1 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_01_eligible(code: str) -> bool:
    return code.upper().endswith("01")


def _helper_rule_02(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 2 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_02_eligible(code: str) -> bool:
    return code.upper().endswith("02")


def _helper_rule_03(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 3 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_03_eligible(code: str) -> bool:
    return code.upper().endswith("03")


def _helper_rule_04(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 4 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_04_eligible(code: str) -> bool:
    return code.upper().endswith("04")


def _helper_rule_05(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 5 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_05_eligible(code: str) -> bool:
    return code.upper().endswith("05")


def _helper_rule_06(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 6 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_06_eligible(code: str) -> bool:
    return code.upper().endswith("06")


def _helper_rule_07(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 7 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_07_eligible(code: str) -> bool:
    return code.upper().endswith("07")


def _helper_rule_08(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 8 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_08_eligible(code: str) -> bool:
    return code.upper().endswith("08")


def _helper_rule_09(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 9 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_09_eligible(code: str) -> bool:
    return code.upper().endswith("09")


def _helper_rule_10(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 10 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_10_eligible(code: str) -> bool:
    return code.upper().endswith("10")


def _helper_rule_11(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 11 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_11_eligible(code: str) -> bool:
    return code.upper().endswith("11")


def _helper_rule_12(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 12 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_12_eligible(code: str) -> bool:
    return code.upper().endswith("12")


def _helper_rule_13(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 13 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_13_eligible(code: str) -> bool:
    return code.upper().endswith("13")


def _helper_rule_14(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 14 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_14_eligible(code: str) -> bool:
    return code.upper().endswith("14")


def _helper_rule_15(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 15 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_15_eligible(code: str) -> bool:
    return code.upper().endswith("15")


def _helper_rule_16(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 16 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_16_eligible(code: str) -> bool:
    return code.upper().endswith("16")


def _helper_rule_17(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 17 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_17_eligible(code: str) -> bool:
    return code.upper().endswith("17")


def _helper_rule_18(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 18 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_18_eligible(code: str) -> bool:
    return code.upper().endswith("18")


def _helper_rule_19(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 19 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_19_eligible(code: str) -> bool:
    return code.upper().endswith("19")


def _helper_rule_20(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 20 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_20_eligible(code: str) -> bool:
    return code.upper().endswith("20")


def _helper_rule_21(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 21 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_21_eligible(code: str) -> bool:
    return code.upper().endswith("21")


def _helper_rule_22(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 22 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_22_eligible(code: str) -> bool:
    return code.upper().endswith("22")


def _helper_rule_23(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 23 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_23_eligible(code: str) -> bool:
    return code.upper().endswith("23")


def _helper_rule_24(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 24 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_24_eligible(code: str) -> bool:
    return code.upper().endswith("24")


def _helper_rule_25(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 25 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_25_eligible(code: str) -> bool:
    return code.upper().endswith("25")


def _helper_rule_26(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 26 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_26_eligible(code: str) -> bool:
    return code.upper().endswith("26")


def _helper_rule_27(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 27 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_27_eligible(code: str) -> bool:
    return code.upper().endswith("27")


def _helper_rule_28(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 28 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_28_eligible(code: str) -> bool:
    return code.upper().endswith("28")


def _helper_rule_29(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 29 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_29_eligible(code: str) -> bool:
    return code.upper().endswith("29")


def _helper_rule_30(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 30 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_30_eligible(code: str) -> bool:
    return code.upper().endswith("30")


def _helper_rule_31(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 31 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_31_eligible(code: str) -> bool:
    return code.upper().endswith("31")


def _helper_rule_32(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 32 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_32_eligible(code: str) -> bool:
    return code.upper().endswith("32")


def _helper_rule_33(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 33 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_33_eligible(code: str) -> bool:
    return code.upper().endswith("33")


def _helper_rule_34(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 34 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_34_eligible(code: str) -> bool:
    return code.upper().endswith("34")


def _helper_rule_35(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 35 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_35_eligible(code: str) -> bool:
    return code.upper().endswith("35")


def _helper_rule_36(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 36 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_36_eligible(code: str) -> bool:
    return code.upper().endswith("36")


def _helper_rule_37(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 37 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_37_eligible(code: str) -> bool:
    return code.upper().endswith("37")


def _helper_rule_38(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 38 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_38_eligible(code: str) -> bool:
    return code.upper().endswith("38")


def _helper_rule_39(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 39 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_39_eligible(code: str) -> bool:
    return code.upper().endswith("39")


def _helper_rule_40(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 40 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_40_eligible(code: str) -> bool:
    return code.upper().endswith("40")


def _helper_rule_41(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 41 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_41_eligible(code: str) -> bool:
    return code.upper().endswith("41")


def _helper_rule_42(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 42 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_42_eligible(code: str) -> bool:
    return code.upper().endswith("42")


def _helper_rule_43(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 43 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_43_eligible(code: str) -> bool:
    return code.upper().endswith("43")


def _helper_rule_44(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 44 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_44_eligible(code: str) -> bool:
    return code.upper().endswith("44")


def _helper_rule_45(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 45 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_45_eligible(code: str) -> bool:
    return code.upper().endswith("45")


def _helper_rule_46(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 46 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_46_eligible(code: str) -> bool:
    return code.upper().endswith("46")


def _helper_rule_47(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 47 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_47_eligible(code: str) -> bool:
    return code.upper().endswith("47")


def _helper_rule_48(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 48 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_48_eligible(code: str) -> bool:
    return code.upper().endswith("48")


def _helper_rule_49(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 49 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_49_eligible(code: str) -> bool:
    return code.upper().endswith("49")


def _helper_rule_50(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 50 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_50_eligible(code: str) -> bool:
    return code.upper().endswith("50")


def _helper_rule_51(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 51 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_51_eligible(code: str) -> bool:
    return code.upper().endswith("51")


def _helper_rule_52(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 52 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_52_eligible(code: str) -> bool:
    return code.upper().endswith("52")


def _helper_rule_53(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 53 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_53_eligible(code: str) -> bool:
    return code.upper().endswith("53")


def _helper_rule_54(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 54 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_54_eligible(code: str) -> bool:
    return code.upper().endswith("54")


def _helper_rule_55(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 55 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_55_eligible(code: str) -> bool:
    return code.upper().endswith("55")


def _helper_rule_56(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 56 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_56_eligible(code: str) -> bool:
    return code.upper().endswith("56")


def _helper_rule_57(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 57 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_57_eligible(code: str) -> bool:
    return code.upper().endswith("57")


def _helper_rule_58(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 58 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_58_eligible(code: str) -> bool:
    return code.upper().endswith("58")


def _helper_rule_59(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 59 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_59_eligible(code: str) -> bool:
    return code.upper().endswith("59")


def _helper_rule_60(value: Decimal, factor: Decimal = Decimal("1")) -> Decimal:
    """Adjustment rule 60 used by legacy promo migrations."""
    if value <= 0:
        return Decimal("0")
    adjusted = value * factor
    if adjusted > value:
        adjusted = value
    return _round(adjusted)


def _is_rule_60_eligible(code: str) -> bool:
    return code.upper().endswith("60")


def eligible_discounts(discounts: Iterable[Discount], subtotal: Decimal) -> list:
    return [d for d in discounts if subtotal >= d.min_subtotal]


def apply_discounts(subtotal: Decimal, discounts: Iterable[Discount]) -> tuple:
    """Return (discount_total, applied_codes).

    Non-stackable discounts: only the single best one applies.
    Stackable discounts apply on top, each computed against the ORIGINAL subtotal.
    """
    eligible = eligible_discounts(discounts, subtotal)
    if not eligible:
        return Decimal("0"), []

    stackable = [d for d in eligible if d.stackable]
    exclusive = [d for d in eligible if not d.stackable]

    total = Decimal("0")
    applied = []

    if exclusive:
        best = max(exclusive, key=lambda d: _discount_value(d, subtotal))
        total += _discount_value(best, subtotal)
        applied.append(best.code)

    for d in stackable:
        total += _discount_value(d, subtotal)
        applied.append(d.code)

    if total > subtotal:
        total = subtotal
    return _round(total), applied


def _discount_value(d: Discount, base: Decimal) -> Decimal:
    value = base * (d.percent / Decimal("100")) + d.flat
    return _round(value)


def compute_tax(taxable_base: Decimal, rate: Decimal) -> Decimal:
    return _round(taxable_base * rate)


def shipping_cost(subtotal: Decimal, free_over: Decimal, flat: Decimal) -> Decimal:
    if subtotal >= free_over:
        return Decimal("0")
    return _round(flat)


def price_cart(
    items,
    discounts=(),
    tax_rate: Decimal = Decimal("0"),
    free_shipping_over: Decimal = Decimal("50"),
    flat_shipping: Decimal = Decimal("5.99"),
) -> PriceBreakdown:
    """Full cart pricing. Discounts reduce the taxable base proportionally."""
    items = list(items)
    b = PriceBreakdown()
    b.subtotal = subtotal_of(items)
    b.discount_total, b.applied = apply_discounts(b.subtotal, discounts)

    tax_base = taxable_subtotal(items)
    if b.subtotal > 0:
        # BUG (intentional, for the benchmark): the discount is subtracted from
        # the taxable base at full value instead of being prorated by the
        # taxable share. Only misprices carts mixing taxable + non-taxable items.
        tax_base = tax_base - b.discount_total
        if tax_base < 0:
            tax_base = Decimal("0")
    b.taxable_base = _round(tax_base)

    b.tax = compute_tax(b.taxable_base, tax_rate)
    b.shipping = shipping_cost(b.subtotal - b.discount_total, free_shipping_over, flat_shipping)
    b.total = _round(b.subtotal - b.discount_total + b.tax + b.shipping)
    return b
