import { backendFirst } from '../request'
import { currentUser } from '../mock-data'

export function demoLogin() {
  return backendFirst({
    url: '/api/auth/demo-login',
    method: 'POST'
  }, () => ({
    token: 'demo-token',
    userInfo: currentUser
  }))
}

export function passwordLogin(payload) {
  return backendFirst({
    url: '/api/auth/password-login',
    method: 'POST',
    data: {
      username: payload.username,
      password: payload.password
    }
  }, () => ({
    token: 'demo-token',
    userInfo: currentUser
  }))
}

export function registerByPassword(payload) {
  return backendFirst({
    url: '/api/auth/register',
    method: 'POST',
    data: {
      username: payload.username,
      password: payload.password,
      nickname: payload.nickname || ''
    }
  }, () => ({
    id: String(currentUser.id),
    username: payload.username,
    nickname: payload.nickname || currentUser.nickname,
    phone: '',
    avatar: currentUser.avatar,
    createdAt: new Date().toISOString()
  }))
}
