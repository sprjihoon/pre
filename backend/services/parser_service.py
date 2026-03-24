import pandas as pd
from datetime import date

REQUIRED_COLUMNS = {
    "주문일": "order_date",
    "업체코드": "supplier_code",
    "업체명": "supplier_name",
    "SKU코드": "sku_code",
    "SKU명": "sku_name",
    "옵션": "option_name",
    "수량": "quantity",
}

COLUMN_ALIASES = {
    "주문일자": "주문일",
    "주문날짜": "주문일",
    "공급처코드": "업체코드",
    "공급처명": "업체명",
    "상품코드": "SKU코드",
    "상품명": "SKU명",
    "옵션명": "옵션",
    "주문수량": "수량",
}


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip()
    rename_map = {}
    for col in df.columns:
        if col in COLUMN_ALIASES:
            rename_map[col] = COLUMN_ALIASES[col]
    if rename_map:
        df = df.rename(columns=rename_map)
    return df


def _validate_columns(df: pd.DataFrame) -> list[str]:
    missing = []
    optional = {"옵션"}
    for kcol in REQUIRED_COLUMNS:
        if kcol not in df.columns and kcol not in optional:
            missing.append(kcol)
    return missing


def _build_combination_key(row: pd.Series) -> str:
    parts = [str(row.get("SKU코드", "")), str(row.get("옵션", "") or "")]
    return "|".join(p for p in parts if p)


def parse_file(file_path: str, ext: str) -> list[dict]:
    if ext == ".csv":
        df = pd.read_csv(file_path, dtype=str)
    else:
        df = pd.read_excel(file_path, dtype=str)

    df = _normalize_columns(df)

    missing = _validate_columns(df)
    if missing:
        raise ValueError(f"필수 컬럼 누락: {', '.join(missing)}")

    if "옵션" not in df.columns:
        df["옵션"] = None

    records = []
    for _, row in df.iterrows():
        try:
            order_date = pd.to_datetime(row["주문일"]).date()
        except Exception:
            continue

        try:
            qty = int(float(row["수량"]))
        except (ValueError, TypeError):
            qty = 0

        if qty <= 0:
            continue

        records.append({
            "order_date": order_date,
            "supplier_code": str(row["업체코드"]).strip(),
            "supplier_name": str(row["업체명"]).strip(),
            "sku_code": str(row["SKU코드"]).strip(),
            "sku_name": str(row["SKU명"]).strip(),
            "option_name": str(row["옵션"]).strip() if pd.notna(row["옵션"]) else None,
            "quantity": qty,
            "combination_key": _build_combination_key(row),
        })

    return records
