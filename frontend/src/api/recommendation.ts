import api from "./client";
import type { Recommendation, Approval, Execution } from "../types";

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
