import api from "./client";
import type { LocationMaster, LocationHistory, PrepackStock } from "../types";

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
