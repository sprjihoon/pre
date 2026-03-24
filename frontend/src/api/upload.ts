import api from "./client";
import type { UploadFile, UploadRecord } from "../types";

export const uploadApi = {
  upload: (file: File) => {
    const fd = new FormData();
    fd.append("file", file);
    return api.post<UploadFile>("/upload", fd, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  list: (activeOnly = true) =>
    api.get<UploadFile[]>("/upload", { params: { active_only: activeOnly } }),
  get: (id: number) => api.get<UploadFile>(`/upload/${id}`),
  records: (id: number, skip = 0, limit = 100) =>
    api.get<UploadRecord[]>(`/upload/${id}/records`, { params: { skip, limit } }),
};
