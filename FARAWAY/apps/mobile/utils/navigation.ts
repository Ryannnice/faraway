import { ROUTES } from "@/constants/routes";

export function go(url: string): void {
  uni.navigateTo({ url });
}

export function goHome(): void {
  uni.reLaunch({ url: ROUTES.home });
}

export function safeBack(fallback = ROUTES.home): void {
  const pages = getCurrentPages();
  if (pages.length > 1) {
    uni.navigateBack();
    return;
  }
  uni.reLaunch({ url: fallback });
}
