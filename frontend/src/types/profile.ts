export interface SupplierProfile {
  id: number;
  supplier_code: string;
  supplier_name: string;
  min_prepack_qty: number;
  combination_priority: boolean;
  recent_weight: number;
  weekday_weight: number;
  new_sku_exclude_days: number;
  overpredict_penalty: number;
  conservative_mode: boolean;
  preferred_model: string | null;
  llm_review_level: string;
}
