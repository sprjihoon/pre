import api from "./client";
import type { DLModel, BacktestResult } from "../types";

export const dlApi = {
  train: (body: { model_type?: string; supplier_code?: string; epochs?: number; batch_size?: number; learning_rate?: number; lookback_days?: number }) =>
    api.post<DLModel>("/dl/train", body),
  predict: (body: { model_id: number; target_date: string; supplier_code?: string }) =>
    api.post("/dl/predict", body),
  backtest: (body: { model_id: number; test_start: string; test_end: string; supplier_code?: string }) =>
    api.post<BacktestResult>("/dl/backtest", body),
  models: (status?: string) => api.get<DLModel[]>("/dl/models", { params: { status } }),
  activate: (id: number) => api.post<DLModel>(`/dl/models/${id}/activate`),
  backtests: (id: number) => api.get<BacktestResult[]>(`/dl/models/${id}/backtests`),
  compare: (modelIds: number[]) => api.post("/dl/compare", modelIds),
};
