import api from "./client";
import type {
  UploadFile,
  UploadRecord,
  SkuAnalysis,
  CombinationAnalysis,
  Recommendation,
  Approval,
  Execution,
  LocationMaster,
  LocationHistory,
  PrepackStock,
  ValidationResult,
  ReportSummary,
  SupplierProfile,
  DLModel,
  BacktestResult,
  DashboardSummary,
} from "../types";

export const uploadApi = {
  upload: (file: File) => {
    const fd = new FormData();
    fd.append("file", file);
    return api.post<UploadFile>("/upload", fd, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  list: (activeOnly = true) =>
    api.get<UploadFile[]>("/upload", { params: { active_only: activeOnly } }),
  get: (id: number) => api.get<UploadFile>(`/upload/${id}`),
  records: (id: number, skip = 0, limit = 100) =>
    api.get<UploadRecord[]>(`/upload/${id}/records`, { params: { skip, limit } }),
};

export const analysisApi = {
  runSku: (date?: string, supplierCode?: string) =>
    api.post<SkuAnalysis[]>("/analysis/sku", null, {
      params: { analysis_date: date, supplier_code: supplierCode },
    }),
  runCombination: (date?: string, supplierCode?: string) =>
    api.post<CombinationAnalysis[]>("/analysis/combination", null, {
      params: { analysis_date: date, supplier_code: supplierCode },
    }),
  listSku: (supplierCode?: string, date?: string) =>
    api.get<SkuAnalysis[]>("/analysis/sku", {
      params: { supplier_code: supplierCode, analysis_date: date },
    }),
  listCombination: (supplierCode?: string, date?: string) =>
    api.get<CombinationAnalysis[]>("/analysis/combination", {
      params: { supplier_code: supplierCode, analysis_date: date },
    }),
};

export const rulesApi = {
  generate: (date?: string, supplierCode?: string) =>
    api.post<Recommendation[]>("/rules/generate", null, {
      params: { target_date: date, supplier_code: supplierCode },
    }),
};

export const recommendationApi = {
  list: (params?: { target_date?: string; supplier_code?: string; status?: string }) =>
    api.get<Recommendation[]>("/recommendation", { params }),
  approve: (id: number, body: { action: string; approved_qty?: number; memo?: string }) =>
    api.post<Approval>(`/recommendation/${id}/approve`, body),
  execute: (id: number, actual_packed_qty: number) =>
    api.post<Execution>(`/recommendation/${id}/execute`, { actual_packed_qty }),
  updateExecution: (execId: number, body: { used_qty?: number; remaining_qty?: number; status?: string }) =>
    api.patch<Execution>(`/recommendation/execution/${execId}`, body),
};

export const locationApi = {
  list: (zone?: string) => api.get<LocationMaster[]>("/location", { params: { zone } }),
  create: (body: { location_code: string; zone?: string; description?: string }) =>
    api.post<LocationMaster>("/location", body),
  assign: (id: number, body: { target_key: string; target_type: string; quantity: number; memo?: string }) =>
    api.post<LocationHistory>(`/location/${id}/assign`, body),
  clear: (id: number, memo?: string) =>
    api.post<LocationHistory>(`/location/${id}/clear`, null, { params: { memo } }),
  history: (id: number) => api.get<LocationHistory[]>(`/location/${id}/history`),
};

export const stockApi = {
  list: (supplierCode?: string, status?: string) =>
    api.get<PrepackStock[]>("/stock", { params: { supplier_code: supplierCode, status } }),
  deduct: (id: number, qty: number) =>
    api.post<PrepackStock>(`/stock/${id}/deduct`, null, { params: { qty } }),
  unwrap: (body: { stock_id: number; unwrap_qty: number; reason?: string; is_returned?: boolean; return_location?: string }) =>
    api.post("/stock/unwrap", body),
  unwrapRecords: (stockId?: number) =>
    api.get("/stock/unwrap-records", { params: { stock_id: stockId } }),
};

export const validationApi = {
  run: (targetDate: string, supplierCode?: string) =>
    api.post<ValidationResult[]>("/validation/run", null, {
      params: { target_date: targetDate, supplier_code: supplierCode },
    }),
  list: (targetDate?: string, supplierCode?: string) =>
    api.get<ValidationResult[]>("/validation", {
      params: { target_date: targetDate, supplier_code: supplierCode },
    }),
};

export const reportApi = {
  summary: (periodStart: string, periodEnd: string, supplierCode?: string) =>
    api.get<ReportSummary>("/report/summary", {
      params: { period_start: periodStart, period_end: periodEnd, supplier_code: supplierCode },
    }),
};

export const printApi = {
  workOrderUrl: (targetDate: string, supplierCode?: string) => {
    let url = `/api/print/work-order?target_date=${targetDate}`;
    if (supplierCode) url += `&supplier_code=${supplierCode}`;
    return url;
  },
};

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

export const llmApi = {
  review: (recommendationIds: number[], reviewLevel = "light") =>
    api.post("/llm/review", { recommendation_ids: recommendationIds, review_level: reviewLevel }),
  reviews: (recommendationId?: number, reviewType?: string) =>
    api.get("/llm/reviews", { params: { recommendation_id: recommendationId, review_type: reviewType } }),
};

export const profileApi = {
  list: () => api.get<SupplierProfile[]>("/profile"),
  get: (code: string) => api.get<SupplierProfile>(`/profile/${code}`),
  create: (body: Partial<SupplierProfile>) => api.post<SupplierProfile>("/profile", body),
  update: (code: string, body: Partial<SupplierProfile>) => api.patch<SupplierProfile>(`/profile/${code}`, body),
  delete: (code: string) => api.delete(`/profile/${code}`),
  exclusions: (supplierCode?: string) =>
    api.get("/profile/exclusions/list", { params: { supplier_code: supplierCode } }),
  addExclusion: (body: { supplier_code: string; target_type: string; target_key: string; reason?: string; exclude_until?: string }) =>
    api.post("/profile/exclusions", body),
  removeExclusion: (id: number) => api.delete(`/profile/exclusions/${id}`),
};

export const dashboardApi = {
  summary: () => api.get<DashboardSummary>("/dashboard/summary"),
};
