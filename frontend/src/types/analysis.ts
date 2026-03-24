export interface SkuAnalysis {
  id: number;
  sku_code: string;
  supplier_code: string;
  analysis_date: string;
  avg_7d: number;
  avg_30d: number;
  avg_same_weekday: number;
  repetition_rate: number;
  volatility: number;
  total_days_appeared: number;
  consecutive_days: number;
}

export interface CombinationAnalysis {
  id: number;
  combination_key: string;
  supplier_code: string;
  analysis_date: string;
  occurrence_rate: number;
  avg_quantity: number;
  repetition_rate: number;
  total_occurrences: number;
}
