from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import upload, analysis, rules, recommendation, location, stock, validation, report, print as print_router, deep_learning, llm, profile


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="프리패킹 예측 및 운영관리 시스템",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(analysis.router)
app.include_router(rules.router)
app.include_router(recommendation.router)
app.include_router(location.router)
app.include_router(stock.router)
app.include_router(validation.router)
app.include_router(report.router)
app.include_router(print_router.router)
app.include_router(deep_learning.router)
app.include_router(llm.router)
app.include_router(profile.router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.get("/api/dashboard/summary")
async def dashboard_summary():
    from sqlalchemy import select, func
    from database import async_session
    from models.upload import UploadFile
    from models.recommendation import Recommendation
    from models.stock import PrepackStock
    from models.validation import ValidationResult

    async with async_session() as db:
        uploads = await db.execute(select(func.count(UploadFile.id)).where(UploadFile.is_active == True))
        recs = await db.execute(select(func.count(Recommendation.id)))
        pending = await db.execute(select(func.count(Recommendation.id)).where(Recommendation.status == "pending"))
        stocks = await db.execute(select(func.count(PrepackStock.id)).where(PrepackStock.status == "active"))
        vals = await db.execute(select(func.avg(ValidationResult.accuracy)))

        return {
            "active_uploads": uploads.scalar() or 0,
            "total_recommendations": recs.scalar() or 0,
            "pending_recommendations": pending.scalar() or 0,
            "active_stocks": stocks.scalar() or 0,
            "avg_accuracy": round(float(vals.scalar() or 0), 4),
        }
