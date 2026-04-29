<script setup lang="ts">
import { onPullDownRefresh, onShow } from "@dcloudio/uni-app";

import AppNavBar from "@/components/AppNavBar.vue";
import { ROUTES } from "@/constants/routes";
import { useAuthGuard } from "@/composables/useAuthGuard";
import { useNotificationStore } from "@/stores/notification";
import { formatDateTime } from "@/utils/format";
import { go } from "@/utils/navigation";

useAuthGuard();

const notificationStore = useNotificationStore();

async function refresh() {
  try {
    await notificationStore.fetchList();
  } catch (error) {
    uni.showToast({
      title: error instanceof Error ? error.message : "加载失败",
      icon: "none",
    });
  }
}

onShow(() => {
  void refresh();
});

onPullDownRefresh(async () => {
  await refresh();
  uni.stopPullDownRefresh();
});
</script>

<template>
  <view class="page-shell">
    <AppNavBar title="通知" subtitle="Notifications" />

    <view v-if="notificationStore.list.length" class="card-stack">
      <view
        v-for="item in notificationStore.list"
        :key="item.id"
        class="glass-card notice-card"
        @tap="go(ROUTES.match)"
      >
        <text class="notice-title">{{ item.title }}</text>
        <text class="notice-content">{{ item.content }}</text>
        <text class="notice-meta">{{ formatDateTime(item.created_at) }}</text>
      </view>
    </view>

    <view v-else class="glass-card notice-card empty-card">
      <text class="notice-title">还没有通知</text>
      <text class="notice-content">候选出现和确认成功后会在这里留下记录。</text>
    </view>
  </view>
</template>

<style scoped lang="scss">
.notice-card {
  border-radius: 30rpx;
  padding: 28rpx;
}

.empty-card {
  margin-top: 40rpx;
}

.notice-title {
  display: block;
  font-size: 30rpx;
  font-weight: 700;
}

.notice-content {
  display: block;
  margin-top: 12rpx;
  color: rgba(246, 240, 232, 0.72);
  line-height: 1.6;
}

.notice-meta {
  display: block;
  margin-top: 18rpx;
  color: rgba(246, 240, 232, 0.42);
  font-size: 22rpx;
}
</style>
