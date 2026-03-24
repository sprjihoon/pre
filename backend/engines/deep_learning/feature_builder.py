"""학습/예측용 피처 빌더 - 시계열 데이터를 텐서로 변환"""

import numpy as np
from datetime import date, timedelta
from collections import defaultdict


def build_features(
    records: list[dict],
    target_date: date,
    lookback_days: int = 30,
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """
    레코드 목록에서 (samples, lookback, features) 형태의 X와 (samples,) 형태의 y를 생성.
    returns: (X, y, target_keys)
    """
    by_key: dict[str, dict[date, int]] = defaultdict(lambda: defaultdict(int))
    for r in records:
        key = r.get("sku_code", r.get("target_key", ""))
        d = r["order_date"] if isinstance(r["order_date"], date) else date.fromisoformat(str(r["order_date"]))
        by_key[key][d] += r.get("quantity", 0)

    date_range = [target_date - timedelta(days=i) for i in range(lookback_days + 1, 0, -1)]

    X_list = []
    y_list = []
    keys_list = []

    for key, date_qty in by_key.items():
        if len(date_qty) < 7:
            continue

        seq = []
        for d in date_range[:-1]:
            qty = date_qty.get(d, 0)
            weekday = d.weekday() / 6.0
            seq.append([float(qty), weekday])

        target_qty = date_qty.get(date_range[-1], 0)

        X_list.append(seq)
        y_list.append(float(target_qty))
        keys_list.append(key)

    if not X_list:
        return np.array([]), np.array([]), []

    return np.array(X_list, dtype=np.float32), np.array(y_list, dtype=np.float32), keys_list
