from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import (
    upload, analysis, rules, recommendation,
    location, stock, validation, report,
    print as print_router, deep_learning, llm, profile, dashboard,
)


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
app.include_router(dashboard.router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
