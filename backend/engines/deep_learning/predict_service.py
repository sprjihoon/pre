import torch
from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.deep_learning import DLModel
from models.upload import UploadRecord, UploadFile
from engines.deep_learning.feature_builder import build_features
from engines.deep_learning.models.lstm_model import PrepackLSTM
from engines.deep_learning.models.transformer_model import PrepackTransformer
from schemas.deep_learning import PredictResult


async def predict(
    db: AsyncSession,
    model_id: int,
    target_date: date,
    supplier_code: str | None = None,
) -> list[PredictResult]:
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

    records = [
        {"sku_code": r.sku_code, "order_date": r.order_date, "quantity": r.quantity}
        for r in records_orm
    ]

    X, _, keys = build_features(records, target_date, lookback)
    if len(X) == 0:
        return []

    if dl_model.model_type == "transformer":
        model = PrepackTransformer(input_size=input_size)
    else:
        model = PrepackLSTM(input_size=input_size)

    model.load_state_dict(torch.load(dl_model.file_path, weights_only=True))
    model.eval()

    X_tensor = torch.FloatTensor(X)
    with torch.no_grad():
        predictions = model(X_tensor).numpy()

    results = []
    for key, pred in zip(keys, predictions):
        qty = max(0, round(float(pred)))
        conf = min(1.0, max(0.0, 1.0 - abs(float(pred) - qty) / (float(pred) + 1e-6)))
        results.append(PredictResult(
            target_key=key,
            target_type="sku",
            predicted_qty=qty,
            confidence=round(conf, 4),
        ))

    return results
