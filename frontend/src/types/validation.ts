export interface ValidationResult {
  id: number;
  target_date: string;
  supplier_code: string;
  target_key: string;
  predicted_qty: number;
  actual_qty: number;
  accuracy: number;
  usage_rate: number;
  unwrap_rate: number;
  is_overpredict: boolean;
  is_underpredict: boolean;
}

export interface ReportSummary {
  period_start: string;
  period_end: string;
  supplier_code: string | null;
  total_predictions: number;
  avg_accuracy: number;
  avg_usage_rate: number;
  avg_unwrap_rate: number;
  overpredict_count: number;
  underpredict_count: number;
}
