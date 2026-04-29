import { onShow } from "@dcloudio/uni-app";

import { ROUTES } from "@/constants/routes";
import { useAuthStore } from "@/stores/auth";

export function useAuthGuard(): void {
  const authStore = useAuthStore();

  onShow(() => {
    authStore.hydrate();
    if (!authStore.loggedIn) {
      uni.reLaunch({ url: ROUTES.login });
    }
  });
}
