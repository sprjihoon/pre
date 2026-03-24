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
