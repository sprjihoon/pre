import api from "./client";
import type { SupplierProfile } from "../types";

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
