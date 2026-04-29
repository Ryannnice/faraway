import { ROUTES } from "@/constants/routes";
import { clearToken, getToken } from "@/utils/storage";

import type { ApiEnvelope } from "./types";

const API_BASE_URL = "http://127.0.0.1:8000";

function handleAuthExpired(): void {
  clearToken();
  uni.reLaunch({ url: ROUTES.login });
}

export function request<T>(options: {
  url: string;
  method?: "GET" | "POST" | "PUT";
  data?: Record<string, unknown>;
  auth?: boolean;
}): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };
  if (options.auth !== false && token) {
    headers.Authorization = `Bearer ${token}`;
  }

  return new Promise((resolve, reject) => {
    uni.request({
      url: `${API_BASE_URL}${options.url}`,
      method: options.method ?? "GET",
      header: headers,
      data: options.data ?? {},
      success: (response: any) => {
        const body = response.data as ApiEnvelope<T>;
        if (response.statusCode === 401) {
          handleAuthExpired();
        }
        if (response.statusCode >= 200 && response.statusCode < 300 && body.code === 0) {
          resolve(body.data);
          return;
        }
        reject(new Error(body?.message || "请求失败"));
      },
      fail: (error: any) => {
        reject(error);
      },
    });
  });
}

export function uploadImage(filePath: string): Promise<{ asset_id: string; url: string }> {
  const token = getToken();
  return new Promise((resolve, reject) => {
    uni.uploadFile({
      url: `${API_BASE_URL}/api/upload/image`,
      name: "file",
      filePath,
      header: {
        Authorization: `Bearer ${token}`,
      },
      success: (response: any) => {
        const body = JSON.parse(response.data) as ApiEnvelope<{ asset_id: string; url: string }>;
        if (body.code === 0) {
          resolve(body.data);
          return;
        }
        reject(new Error(body.message || "上传失败"));
      },
      fail: (error: any) => {
        reject(error);
      },
    });
  });
}
