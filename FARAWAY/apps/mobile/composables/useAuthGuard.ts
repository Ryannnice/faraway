import { onShow } from "@dcloudio/uni-app";

import { ROUTES } from "@/constants/routes";
import { useAuthStore } from "@/stores/auth";

export function ensureLoggedIn(): boolean {
  const authStore = useAuthStore();
  authStore.hydrate();
  if (authStore.loggedIn) {
    return true;
  }
  uni.reLaunch({ url: ROUTES.login });
  return false;
}

export function useAuthGuard(): void {
  onShow(() => {
    ensureLoggedIn();
  });
}
