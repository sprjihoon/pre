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
