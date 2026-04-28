import { onShow } from '@dcloudio/uni-app'
import { isLoggedIn } from '../utils/auth'
import { ROUTES } from '../constants/routes'

export function useAuthGuard() {
  onShow(() => {
    if (!isLoggedIn()) {
      uni.reLaunch({ url: ROUTES.login })
    }
  })
}
