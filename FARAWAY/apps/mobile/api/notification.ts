import { request } from "./request";
import type { NotificationItem } from "./types";

export function getNotifications() {
  return request<{ list: NotificationItem[] }>({
    url: "/api/my/notifications",
  });
}
