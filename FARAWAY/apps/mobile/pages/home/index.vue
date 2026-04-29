<script setup>
import { computed } from "vue";

import { ROUTES } from "@/constants/routes";
import { useAuthGuard } from "@/composables/useAuthGuard";
import { useAuthStore } from "@/stores/auth";
import { go } from "@/utils/navigation";

useAuthGuard();

const authStore = useAuthStore();
const nickname = computed(() => {
  const userInfo = authStore.userInfo;
  return userInfo && userInfo.nickname ? userInfo.nickname : "旅人";
});
const heroImage =
  "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&q=80&w=2000";
</script>

<template>
  <view class="home-page">
    <image class="hero-bg" :src="heroImage" mode="aspectFill" />
    <view class="hero-mask" />

    <view class="hero-content">
      <text class="section-kicker">Faraway Polaris</text>
      <text class="hero-title">你好，{{ nickname }}。</text>
      <text class="hero-copy">先决定怎么出发，再决定和谁一起出发。</text>

      <view class="cta-row">
        <view class="pill-button cta" @tap="go(ROUTES.strategy)">做攻略</view>
        <view class="pill-button cta accent" @tap="go(ROUTES.match)">找搭子</view>
      </view>

      <view class="quick-links glass-card">
        <view class="quick-link" @tap="go(ROUTES.myPartners)">
          <text class="quick-title">我的搭子</text>
          <text class="quick-copy">查看当前匹配和已确认赴约</text>
        </view>
        <view class="quick-link" @tap="go(ROUTES.notice)">
          <text class="quick-title">通知</text>
          <text class="quick-copy">候选出现和确认成功都会留痕</text>
        </view>
        <view class="quick-link" @tap="go(ROUTES.profile)">
          <text class="quick-title">个人资料</text>
          <text class="quick-copy">头像、昵称、简介都在这里维护</text>
        </view>
      </view>
    </view>
  </view>
</template>

<style scoped lang="scss">
.home-page {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

.hero-bg,
.hero-mask {
  position: absolute;
  inset: 0;
}

.hero-bg {
  width: 100%;
  height: 80vh;
}

.hero-mask {
  background: linear-gradient(180deg, rgba(7, 17, 31, 0.12) 0%, rgba(7, 17, 31, 0.24) 52%, #07111f 100%);
}

.hero-content {
  position: relative;
  z-index: 2;
  padding: 120rpx 28rpx 100rpx;
}

.hero-title {
  display: block;
  margin-top: 24rpx;
  font-size: 64rpx;
  line-height: 1.08;
  font-weight: 700;
  color: #f6f0e8;
}

.hero-copy {
  display: block;
  margin-top: 24rpx;
  width: 78%;
  font-size: 30rpx;
  line-height: 1.6;
  color: rgba(246, 240, 232, 0.72);
}

.cta-row {
  display: flex;
  gap: 20rpx;
  margin-top: 36rpx;
}

.cta {
  min-width: 200rpx;
}

.accent {
  background: rgba(236, 214, 179, 0.18);
}

.quick-links {
  margin-top: 72rpx;
  border-radius: 34rpx;
  padding: 20rpx 28rpx;
}

.quick-link {
  padding: 24rpx 0;
  border-bottom: 1rpx solid rgba(255, 255, 255, 0.08);
}

.quick-link:last-child {
  border-bottom: none;
}

.quick-title {
  display: block;
  font-size: 30rpx;
  font-weight: 700;
}

.quick-copy {
  display: block;
  margin-top: 10rpx;
  font-size: 24rpx;
  color: rgba(246, 240, 232, 0.68);
}
</style>
