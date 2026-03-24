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
