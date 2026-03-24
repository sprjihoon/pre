import os
import torch
import torch.nn as nn
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.deep_learning import DLModel
from models.upload import UploadRecord, UploadFile
from engines.deep_learning.feature_builder import build_features
from engines.deep_learning.models.lstm_model import PrepackLSTM
from engines.deep_learning.models.transformer_model import PrepackTransformer


async def train_model(
    db: AsyncSession,
    model_type: str = "lstm",
    supplier_code: str | None = None,
    epochs: int = 50,
    batch_size: int = 32,
    learning_rate: float = 0.001,
    lookback_days: int = 30,
) -> DLModel:
    q = select(UploadRecord).join(UploadFile).where(UploadFile.is_active == True)
    if supplier_code:
        q = q.where(UploadRecord.supplier_code == supplier_code)
    result = await db.execute(q)
    records_orm = result.scalars().all()

    records = [
        {"sku_code": r.sku_code, "order_date": r.order_date, "quantity": r.quantity}
        for r in records_orm
    ]

    if not records:
        raise ValueError("학습할 데이터가 없습니다.")

    from datetime import date as date_type
    all_dates = sorted(set(r["order_date"] for r in records))
    if len(all_dates) < lookback_days + 5:
        raise ValueError(f"최소 {lookback_days + 5}일 이상의 데이터가 필요합니다.")

    split_idx = int(len(all_dates) * 0.8)
    train_end = all_dates[split_idx]

    train_records = [r for r in records if r["order_date"] <= train_end]
    X, y, keys = build_features(train_records, train_end, lookback_days)

    if len(X) == 0:
        raise ValueError("피처 생성에 실패했습니다.")

    X_tensor = torch.FloatTensor(X)
    y_tensor = torch.FloatTensor(y)

    input_size = X_tensor.shape[2]
    if model_type == "transformer":
        model = PrepackTransformer(input_size=input_size)
    else:
        model = PrepackLSTM(input_size=input_size)

    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    loss_fn = nn.MSELoss()

    model.train()
    for epoch in range(epochs):
        for i in range(0, len(X_tensor), batch_size):
            batch_x = X_tensor[i:i + batch_size]
            batch_y = y_tensor[i:i + batch_size]

            pred = model(batch_x)
            loss = loss_fn(pred, batch_y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    model.eval()
    with torch.no_grad():
        all_pred = model(X_tensor)
        mse = loss_fn(all_pred, y_tensor).item()
        accuracy = max(0, 1.0 - (mse ** 0.5) / (y_tensor.mean().item() + 1e-6))

    os.makedirs(settings.MODEL_STORE_DIR, exist_ok=True)
    version = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_name = f"prepack_{model_type}_{version}"
    file_path = os.path.join(settings.MODEL_STORE_DIR, f"{model_name}.pt")
    torch.save(model.state_dict(), file_path)

    dl_model = DLModel(
        model_name=model_name,
        model_version=version,
        model_type=model_type,
        file_path=file_path,
        train_accuracy=round(accuracy, 4),
        trained_at=datetime.now(),
        status="trained",
        training_params={
            "epochs": epochs,
            "batch_size": batch_size,
            "learning_rate": learning_rate,
            "lookback_days": lookback_days,
            "supplier_code": supplier_code,
            "input_size": input_size,
        },
    )
    db.add(dl_model)
    await db.commit()
    await db.refresh(dl_model)
    return dl_model
