import api from "./client";
import type { ValidationResult, ReportSummary } from "../types";

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
