const TOKEN_KEY = 'faraway_token'
const USER_KEY = 'faraway_user'
const SEARCH_HISTORY_KEY = 'faraway_search_history'
const PENDING_DRAFT_KEY = 'faraway_pending_draft'

export function setToken(token) {
  uni.setStorageSync(TOKEN_KEY, token)
}

export function getToken() {
  return uni.getStorageSync(TOKEN_KEY) || ''
}

export function clearToken() {
  uni.removeStorageSync(TOKEN_KEY)
}

export function setUserInfo(userInfo) {
  uni.setStorageSync(USER_KEY, userInfo)
}

export function getUserInfo() {
  return uni.getStorageSync(USER_KEY) || null
}

export function clearUserInfo() {
  uni.removeStorageSync(USER_KEY)
}

export function setPendingDraft(draft) {
  uni.setStorageSync(PENDING_DRAFT_KEY, draft)
}

export function getPendingDraft() {
  return uni.getStorageSync(PENDING_DRAFT_KEY) || null
}

export function clearPendingDraft() {
  uni.removeStorageSync(PENDING_DRAFT_KEY)
}

export function getSearchHistory() {
  return uni.getStorageSync(SEARCH_HISTORY_KEY) || []
}

export function saveSearchKeyword(keyword) {
  const trimmed = (keyword || '').trim()
  if (!trimmed) {
    return
  }
  const history = getSearchHistory().filter((item) => item !== trimmed)
  history.unshift(trimmed)
  uni.setStorageSync(SEARCH_HISTORY_KEY, history.slice(0, 10))
}

export function clearSearchHistory() {
  uni.removeStorageSync(SEARCH_HISTORY_KEY)
}
