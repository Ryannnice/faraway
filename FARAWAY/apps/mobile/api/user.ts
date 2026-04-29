import { request } from "./request";
import type { UserProfile } from "./types";

export function getMyProfile() {
  return request<UserProfile>({
    url: "/api/user/profile",
  });
}

export function updateMyProfile(payload: Partial<Pick<UserProfile, "nickname" | "bio" | "avatar" | "gender">>) {
  return request<UserProfile>({
    url: "/api/user/profile",
    method: "PUT",
    data: payload,
  });
}

export function getUserProfile(userId: string) {
  return request<UserProfile>({
    url: `/api/users/${userId}`,
  });
}
