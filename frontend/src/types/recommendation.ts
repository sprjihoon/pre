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
