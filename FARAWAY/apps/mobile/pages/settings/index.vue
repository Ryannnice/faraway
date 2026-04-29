<script setup lang="ts">
import AppNavBar from "@/components/AppNavBar.vue";
import { ROUTES } from "@/constants/routes";
import { useAuthGuard } from "@/composables/useAuthGuard";
import { useAuthStore } from "@/stores/auth";

useAuthGuard();

const authStore = useAuthStore();

async function handleLogout() {
  await authStore.signOut();
  uni.reLaunch({ url: ROUTES.login });
}
</script>

<template>
  <view class="page-shell">
    <AppNavBar title="设置" subtitle="Settings" />

    <view class="glass-card panel">
      <text class="section-kicker">Session</text>
      <text class="panel-title">退出登录</text>
      <text class="panel-copy">P0 设置页只做一件事：清掉登录态并回到登录页。</text>
      <button class="danger-button action-button" @tap="handleLogout">退出登录</button>
    </view>
  </view>
</template>

<style scoped lang="scss">
.panel {
  border-radius: 34rpx;
  padding: 34rpx;
}

.panel-title {
  display: block;
  margin-top: 12rpx;
  font-size: 34rpx;
  font-weight: 700;
}

.panel-copy {
  display: block;
  margin-top: 16rpx;
  line-height: 1.7;
  color: rgba(246, 240, 232, 0.72);
}

.action-button {
  margin-top: 30rpx;
}
</style>
