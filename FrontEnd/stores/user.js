import { clearToken, clearUserInfo, getToken, getUserInfo, setToken, setUserInfo } from '../utils/storage'

const userStore = {
  token: getToken(),
  userInfo: getUserInfo(),
  login(token, userInfo) {
    this.token = token
    this.userInfo = userInfo
    setToken(token)
    setUserInfo(userInfo)
  },
  setProfile(userInfo) {
    this.userInfo = userInfo
    setUserInfo(userInfo)
  },
  logout() {
    this.token = ''
    this.userInfo = null
    clearToken()
    clearUserInfo()
  }
}

export function useUserStore() {
  return userStore
}
