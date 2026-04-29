import { defineStore } from "pinia";

import { getNotifications } from "@/api/notification";
import type { NotificationItem } from "@/api/types";

export const useNotificationStore = defineStore("notification", {
  state: () => ({
    list: [] as NotificationItem[],
  }),
  actions: {
    async fetchList() {
      const data = await getNotifications();
      this.list = data.list;
      return this.list;
    },
  },
});
