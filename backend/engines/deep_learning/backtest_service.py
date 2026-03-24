"""백테스트 서비스 - 미래 데이터 누출 방지가 핵심"""

import torch
from datetime import date, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.deep_learning import DLModel, BacktestResult
from models.upload import UploadRecord, UploadFile
from engines.deep_learning.feature_builder import build_features
from engines.deep_learning.models.lstm_model import PrepackLSTM
from engines.deep_learning.models.transformer_model import PrepackTransformer


async def run_backtest(
    db: AsyncSession,
    model_id: int,
    test_start: date,
    test_end: date,
    supplier_code: str | None = None,
) -> BacktestResult:
    result = await db.execute(select(DLModel).where(DLModel.id == model_id))
    dl_model = result.scalars().first()
    if not dl_model:
        raise ValueError("모델을 찾을 수 없습니다.")

    params = dl_model.training_params or {}
    lookback = params.get("lookback_days", 30)
    input_size = params.get("input_size", 2)

    q = select(UploadRecord).join(UploadFile).where(UploadFile.is_active == True)
    if supplier_code:
        q = q.where(UploadRecord.supplier_code == supplier_code)
    rec_result = await db.execute(q)
    records_orm = rec_result.scalars().all()

    all_records = [
        {"sku_code": r.sku_code, "order_date": r.order_date, "quantity": r.quantity}
        for r in records_orm
    ]

    if dl_model.model_type == "transformer":
        model = PrepackTransformer(input_size=input_size)
    else:
        model = PrepackLSTM(input_size=input_size)

    model.load_state_dict(torch.load(dl_model.file_path, weights_only=True))
    model.eval()

    total_pred = 0
    correct_pred = 0
    over_count = 0
    under_count = 0
    total_usage = 0.0
    total_unwrap = 0.0
    test_days = 0

    current = test_start
    while current <= test_end:
        # 핵심: 기준일 이전 데이터만 사용
        past_records = [r for r in all_records if r["order_date"] < current]

        X, y_actual, keys = build_features(past_records, current, lookback)
        if len(X) == 0:
            current += timedelta(days=1)
            continue

        X_tensor = torch.FloatTensor(X)
        with torch.no_grad():
            preds = model(X_tensor).numpy()

        for pred_val, actual_val in zip(preds, y_actual):
            pred_qty = max(0, round(float(pred_val)))
            actual_qty = int(actual_val)
            total_pred += 1

            if actual_qty > 0 and abs(pred_qty - actual_qty) / actual_qty <= 0.3:
                correct_pred += 1

            if pred_qty > actual_qty:
                over_count += 1
                total_unwrap += (pred_qty - actual_qty)
            elif pred_qty < actual_qty:
                under_count += 1

            if pred_qty > 0:
                total_usage += min(actual_qty / pred_qty, 1.0)

        test_days += 1
        current += timedelta(days=1)

    sku_accuracy = correct_pred / total_pred if total_pred > 0 else 0.0
    usage_rate = total_usage / total_pred if total_pred > 0 else 0.0
    over_rate = over_count / total_pred if total_pred > 0 else 0.0
    under_rate = under_count / total_pred if total_pred > 0 else 0.0

    bt = BacktestResult(
        model_id=model_id,
        test_start=test_start,
        test_end=test_end,
        supplier_code=supplier_code,
        sku_accuracy=round(sku_accuracy, 4),
        combination_hit_rate=0.0,
        threshold_detection_accuracy=round(sku_accuracy, 4),
        usage_rate=round(usage_rate, 4),
        unwrap_rate=round(1.0 - usage_rate, 4),
        overpredict_rate=round(over_rate, 4),
        underpredict_rate=round(under_rate, 4),
    )
    db.add(bt)
    await db.commit()
    await db.refresh(bt)
    return bt
