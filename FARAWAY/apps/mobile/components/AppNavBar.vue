<script setup>
import { computed } from "vue";

import { safeBack, goHome } from "@/utils/navigation";

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    default: "",
  },
  backable: {
    type: Boolean,
    default: true,
  },
});

const hasSubtitle = computed(() => Boolean(props.subtitle));
</script>

<template>
  <view class="nav-bar">
    <view class="nav-action left" @tap="props.backable ? safeBack() : undefined">
      <text v-if="props.backable" class="nav-button">返回</text>
    </view>
    <view class="nav-center">
      <text class="nav-title">{{ props.title }}</text>
      <text v-if="hasSubtitle" class="nav-subtitle">{{ props.subtitle }}</text>
    </view>
    <view class="nav-action right" @tap="goHome">
      <text class="nav-button">首页</text>
    </view>
  </view>
</template>

<style scoped lang="scss">
.nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28rpx;
}

.nav-action {
  width: 120rpx;
  min-height: 72rpx;
  display: flex;
  align-items: center;
}

.right {
  justify-content: flex-end;
}

.nav-center {
  flex: 1;
  text-align: center;
}

.nav-title {
  display: block;
  font-size: 30rpx;
  font-weight: 700;
  color: #f6f0e8;
}

.nav-subtitle {
  display: block;
  margin-top: 6rpx;
  font-size: 20rpx;
  color: rgba(246, 240, 232, 0.45);
  letter-spacing: 4rpx;
  text-transform: uppercase;
}

.nav-button {
  padding: 14rpx 20rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.08);
  color: #f6f0e8;
  font-size: 22rpx;
}
</style>
