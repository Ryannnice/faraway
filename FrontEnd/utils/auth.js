import { getToken } from './storage'

export function isLoggedIn() {
  return !!getToken()
}
