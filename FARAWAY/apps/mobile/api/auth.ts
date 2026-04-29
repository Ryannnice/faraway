import { request } from "./request";
import type { UserInfo } from "./types";

export function register(payload: { username: string; password: string }) {
  return request<{
    id: string;
    username: string;
    nickname: string;
    avatar: string;
    bio: string;
    gender: string;
    created_at: string;
  }>({
    url: "/api/auth/register",
    method: "POST",
    data: payload,
    auth: false,
  });
}

export function passwordLogin(payload: { username: string; password: string }) {
  return request<{ token: string; user_info: UserInfo }>({
    url: "/api/auth/password-login",
    method: "POST",
    data: payload,
    auth: false,
  });
}

export function logout() {
  return request<{ confirmed: boolean }>({
    url: "/api/auth/logout",
    method: "POST",
  });
}
