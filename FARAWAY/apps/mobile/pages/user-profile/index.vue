<script setup>
import { ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";

import { resolveAssetUrl } from "@/api/request";
import AppNavBar from "@/components/AppNavBar.vue";
import { getUserProfile } from "@/api/user";
import { ensureLoggedIn, useAuthGuard } from "@/composables/useAuthGuard";

useAuthGuard();

const profile = ref(null);

onLoad(async (options) => {
  if (!ensureLoggedIn()) {
    return;
  }
  const userId = options && options.user_id ? options.user_id : "";
  if (!userId) {
    uni.showToast({ title: "缺少用户 ID", icon: "none" });
    return;
  }
  try {
    profile.value = await getUserProfile(userId);
  } catch (error) {
    uni.showToast({
      title: error instanceof Error ? error.message : "加载失败",
      icon: "none",
    });
  }
});
</script>

<template>
  <view class="page-shell">
    <AppNavBar title="TA 的主页" subtitle="User" />

    <view v-if="profile" class="glass-card panel">
      <image v-if="profile.avatar" class="avatar-image" :src="resolveAssetUrl(profile.avatar)" mode="aspectFill" />
      <view v-else class="avatar-fallback">{{ profile.nickname.slice(0, 1) }}</view>
      <text class="panel-title">{{ profile.nickname }}</text>
      <text class="panel-copy">性别：{{ profile.gender }}</text>
      <text class="panel-copy">简介：{{ profile.bio || "这个人还没写简介。" }}</text>
    </view>
  </view>
</template>

<style scoped lang="scss">
.panel {
  border-radius: 34rpx;
  padding: 34rpx;
}

.avatar-image,
.avatar-fallback {
  width: 150rpx;
  height: 150rpx;
  border-radius: 999rpx;
}

.avatar-fallback {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(236, 214, 179, 0.18);
  font-size: 48rpx;
  font-weight: 700;
}

.panel-title {
  display: block;
  margin-top: 24rpx;
  font-size: 38rpx;
  font-weight: 700;
}

.panel-copy {
  display: block;
  margin-top: 16rpx;
  color: rgba(246, 240, 232, 0.72);
  line-height: 1.7;
}
</style>
