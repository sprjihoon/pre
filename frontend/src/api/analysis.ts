import api from "./client";
import type { SkuAnalysis, CombinationAnalysis } from "../types";

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
