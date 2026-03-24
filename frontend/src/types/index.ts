export interface UploadFile {
  id: number;
  filename: string;
  original_filename: string;
  file_type: string;
  date_range_start: string | null;
  date_range_end: string | null;
  uploaded_at: string;
  status: string;
  record_count: number;
  version: number;
  is_active: boolean;
}

export interface UploadRecord {
  id: number;
  order_date: string;
  supplier_code: string;
  supplier_name: string;
  sku_code: string;
  sku_name: string;
  option_name: string | null;
  quantity: number;
  combination_key: string | null;
}

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

export interface Recommendation {
  id: number;
  target_date: string;
  supplier_code: string;
  target_type: string;
  target_key: string;
  rule_based_qty: number;
  dl_predicted_qty: number | null;
  final_recommended_qty: number;
  confidence_score: number | null;
  risk_level: string | null;
  llm_review_result: string | null;
  llm_reason: string | null;
  status: string;
  created_at: string;
}

export interface Approval {
  id: number;
  recommendation_id: number;
  action: string;
  approved_qty: number | null;
  memo: string | null;
  approved_at: string;
}

export interface Execution {
  id: number;
  approval_id: number;
  actual_packed_qty: number;
  used_qty: number;
  remaining_qty: number;
  status: string;
  executed_at: string | null;
  completed_at: string | null;
}

export interface LocationMaster {
  id: number;
  location_code: string;
  zone: string | null;
  description: string | null;
  is_active: boolean;
  current_sku: string | null;
  current_combination: string | null;
}

export interface LocationHistory {
  id: number;
  location_id: number;
  action: string;
  target_key: string | null;
  quantity: number;
  action_at: string;
  memo: string | null;
}

export interface PrepackStock {
  id: number;
  target_type: string;
  target_key: string;
  supplier_code: string;
  current_qty: number;
  location_code: string | null;
  status: string;
  last_updated: string;
}

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

export interface DLModel {
  id: number;
  model_name: string;
  model_version: string;
  model_type: string;
  file_path: string | null;
  train_accuracy: number | null;
  trained_at: string | null;
  status: string;
  training_params: Record<string, unknown> | null;
}

export interface BacktestResult {
  id: number;
  model_id: number;
  test_start: string;
  test_end: string;
  supplier_code: string | null;
  sku_accuracy: number;
  combination_hit_rate: number;
  threshold_detection_accuracy: number;
  usage_rate: number;
  unwrap_rate: number;
  overpredict_rate: number;
  underpredict_rate: number;
  tested_at: string;
}

export interface DashboardSummary {
  active_uploads: number;
  total_recommendations: number;
  pending_recommendations: number;
  active_stocks: number;
  avg_accuracy: number;
}
