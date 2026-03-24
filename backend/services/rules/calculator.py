DEFAULT_MIN_QTY = 5
DEFAULT_RECENT_WEIGHT = 0.7
DEFAULT_WEEKDAY_WEIGHT = 0.3


def calculate_rule_qty(
    avg_7d: float,
    avg_30d: float,
    avg_same_weekday: float,
    repetition_rate: float,
    recent_weight: float = DEFAULT_RECENT_WEIGHT,
    weekday_weight: float = DEFAULT_WEEKDAY_WEIGHT,
    min_qty: int = DEFAULT_MIN_QTY,
    conservative: bool = False,
) -> int:
    base = avg_7d * recent_weight + avg_30d * (1 - recent_weight)
    if avg_same_weekday > 0:
        base = base * (1 - weekday_weight) + avg_same_weekday * weekday_weight

    adjusted = base * repetition_rate
    if conservative:
        adjusted *= 0.85

    qty = max(round(adjusted), 0)
    if qty > 0 and qty < min_qty:
        qty = min_qty

    return qty


def assess_risk(repetition_rate: float, volatility: float) -> str:
    if repetition_rate >= 0.8 and volatility < 0.3:
        return "low"
    elif repetition_rate >= 0.5:
        return "medium"
    return "high"
