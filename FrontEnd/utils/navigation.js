import { ROUTES, TAB_PAGES } from '../constants/routes'

export function go(url) {
  if (TAB_PAGES.includes(url)) {
    uni.switchTab({ url })
    return
  }
  uni.navigateTo({ url })
}

export function safeBack(fallback = ROUTES.home) {
  const pages = getCurrentPages()
  if (pages.length > 1) {
    uni.navigateBack()
    return
  }
  if (TAB_PAGES.includes(fallback)) {
    uni.switchTab({ url: fallback })
    return
  }
  uni.reLaunch({ url: fallback })
}
