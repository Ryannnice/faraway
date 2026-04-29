const TOKEN_KEY = "faraway_token";
const USER_INFO_KEY = "faraway_user_info";
const SEEN_CANDIDATES_KEY = "faraway_seen_candidates";

export function getToken(): string {
  return uni.getStorageSync(TOKEN_KEY) || "";
}

export function setToken(token: string): void {
  uni.setStorageSync(TOKEN_KEY, token);
}

export function clearToken(): void {
  uni.removeStorageSync(TOKEN_KEY);
}

export function getUserInfoStorage<T>(): T | null {
  return uni.getStorageSync(USER_INFO_KEY) || null;
}

export function setUserInfoStorage<T>(value: T): void {
  uni.setStorageSync(USER_INFO_KEY, value);
}

export function clearUserInfoStorage(): void {
  uni.removeStorageSync(USER_INFO_KEY);
}

export function readSeenCandidateIds(): string[] {
  return uni.getStorageSync(SEEN_CANDIDATES_KEY) || [];
}

export function markCandidateSeen(candidateId: string): void {
  const next = Array.from(new Set([...readSeenCandidateIds(), candidateId]));
  uni.setStorageSync(SEEN_CANDIDATES_KEY, next);
}
