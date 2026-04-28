import { clearToken, clearUserInfo, getToken } from '../utils/storage'
import { API_BASE_URL, API_TIMEOUT, ENABLE_BACKEND_FALLBACK } from './config'

export function mockRequest(handler, delay = 180) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(handler())
    }, delay)
  })
}

export function buildUrl(url) {
  if (/^https?:\/\//.test(url)) {
    return url
  }
  return `${API_BASE_URL}${url}`
}

function buildHeaders(header = {}) {
  const token = getToken()
  if (!token || header.Authorization) {
    return header
  }
  return {
    ...header,
    Authorization: `Bearer ${token}`
  }
}

function unwrapResponseBody(body) {
  if (!body || typeof body !== 'object' || !Object.prototype.hasOwnProperty.call(body, 'code')) {
    return body
  }
  if (body.code === 0) {
    return body.data === undefined ? {} : body.data
  }
  const error = new Error(body.message || 'Request failed')
  error.code = body.code
  error.response = body
  throw error
}

function shouldFallbackToMock(error) {
  if (!error || typeof error !== 'object') {
    return true
  }
  if (typeof error.statusCode === 'number' && error.statusCode > 0) {
    return false
  }
  if (Object.prototype.hasOwnProperty.call(error, 'code')) {
    return false
  }
  return true
}

function handleUnauthorized() {
  clearToken()
  clearUserInfo()
  uni.showToast({
    title: '登录已失效，请重新登录',
    icon: 'none'
  })
  setTimeout(() => {
    const pages = getCurrentPages()
    const current = pages && pages.length ? pages[pages.length - 1] : null
    if (!current || current.route !== 'pages/login/index') {
      uni.reLaunch({
        url: '/pages/login/index'
      })
    }
  }, 120)
}

function buildHttpError(response) {
  const body = response && response.data
  const statusCode = response && response.statusCode ? response.statusCode : 0
  const message = body && body.message ? body.message : `HTTP ${statusCode || 'request failed'}`
  const error = new Error(message)
  error.statusCode = statusCode
  error.response = response
  if (body && typeof body === 'object' && Object.prototype.hasOwnProperty.call(body, 'code')) {
    error.code = body.code
  }
  if (statusCode === 401) {
    handleUnauthorized()
  }
  return error
}

export function apiRequest(options) {
  const {
    url,
    method = 'GET',
    data,
    header = {},
    timeout = API_TIMEOUT
  } = options

  return new Promise((resolve, reject) => {
    uni.request({
      url: buildUrl(url),
      method,
      data,
      header: buildHeaders(header),
      timeout,
      success: (response) => {
        const statusCode = response.statusCode || 0
        if (statusCode >= 200 && statusCode < 300) {
          try {
            resolve(unwrapResponseBody(response.data))
          } catch (error) {
            reject(error)
          }
          return
        }
        reject(buildHttpError(response))
      },
      fail: (error) => {
        reject(error)
      }
    })
  })
}

export function backendFirst(requestOptions, mockHandler, delay = 180) {
  if (!ENABLE_BACKEND_FALLBACK) {
    return apiRequest(requestOptions)
  }
  return apiRequest(requestOptions).catch((error) => {
    if (!shouldFallbackToMock(error)) {
      return Promise.reject(error)
    }
    return mockRequest(mockHandler, delay)
  })
}
