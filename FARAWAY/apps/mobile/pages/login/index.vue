<script setup>
import { computed, ref } from "vue";
import { onShow } from "@dcloudio/uni-app";

import { ROUTES } from "@/constants/routes";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();
const mode = ref("login");
const username = ref("");
const password = ref("");
const submitting = ref(false);

const title = computed(() => (mode.value === "login" ? "密码登录" : "注册账号"));

onShow(() => {
  authStore.hydrate();
  if (authStore.loggedIn) {
    uni.reLaunch({ url: ROUTES.home });
  }
});

async function handleSubmit() {
  if (submitting.value) {
    return;
  }
  submitting.value = true;
  try {
    if (mode.value === "login") {
      await authStore.login(username.value, password.value);
    } else {
      await authStore.registerAndLogin(username.value, password.value);
    }
    uni.reLaunch({ url: ROUTES.home });
  } catch (error) {
    uni.showToast({
      title: error instanceof Error ? error.message : "操作失败",
      icon: "none",
    });
  } finally {
    submitting.value = false;
  }
}
</script>

<template>
  <view class="login-page">
    <view class="hero-copy">
      <text class="section-kicker">Faraway</text>
      <text class="hero-title">找攻略，也找一起出发的人。</text>
      <text class="hero-desc">P0 先把注册、实时匹配、攻略生成和赴约确认这一条链路跑通。</text>
    </view>

    <view class="login-card glass-card">
      <view class="mode-row">
        <view class="mode-pill" :class="{ active: mode === 'login' }" @tap="mode = 'login'">登录</view>
        <view class="mode-pill" :class="{ active: mode === 'register' }" @tap="mode = 'register'">注册</view>
      </view>

      <text class="panel-title">{{ title }}</text>

      <view class="field-block">
        <text class="label-text">用户名</text>
        <input v-model="username" class="field-input" placeholder="3-32 位，字母/数字/下划线" />
      </view>

      <view class="field-block">
        <text class="label-text">密码</text>
        <input v-model="password" class="field-input" password placeholder="6-128 位密码" />
      </view>

      <button class="primary-button submit-button" :class="{ 'button-disabled': submitting }" @tap="handleSubmit">
        {{ submitting ? "处理中..." : title }}
      </button>
    </view>
  </view>
</template>

<style scoped lang="scss">
.login-page {
  min-height: 100vh;
  padding: 120rpx 28rpx 60rpx;
  box-sizing: border-box;
}

.hero-copy {
  max-width: 560rpx;
}

.hero-title {
  display: block;
  margin-top: 20rpx;
  font-size: 64rpx;
  line-height: 1.06;
  font-weight: 700;
  color: #f6f0e8;
}

.hero-desc {
  display: block;
  margin-top: 24rpx;
  color: rgba(246, 240, 232, 0.72);
  font-size: 28rpx;
  line-height: 1.6;
}

.login-card {
  margin-top: 48rpx;
  border-radius: 34rpx;
  padding: 32rpx;
}

.mode-row {
  display: flex;
  gap: 12rpx;
}

.mode-pill {
  flex: 1;
  height: 76rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.04);
  color: rgba(246, 240, 232, 0.56);
}

.mode-pill.active {
  background: rgba(236, 214, 179, 0.12);
  color: #f6f0e8;
}

.panel-title {
  display: block;
  margin-top: 28rpx;
  font-size: 34rpx;
  font-weight: 700;
}

.field-block {
  margin-top: 24rpx;
}

.submit-button {
  margin-top: 32rpx;
}
</style>
