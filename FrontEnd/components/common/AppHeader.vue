<template>
  <view class="header">
    <view class="left" @tap="onBack">
      <text v-if="backable" class="back-text">‹</text>
    </view>
    <view class="center">
      <text class="title">{{ title }}</text>
      <text v-if="subtitle" class="subtitle">{{ subtitle }}</text>
    </view>
    <view class="right">
      <slot />
    </view>
  </view>
</template>

<script>
import { safeBack } from '../../utils/navigation'

export default {
  props: {
    title: {
      type: String,
      default: ''
    },
    subtitle: {
      type: String,
      default: ''
    },
    backable: {
      type: Boolean,
      default: true
    },
    fallback: {
      type: String,
      default: '/pages/home/index'
    },
    forceFallback: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    onBack() {
      if (!this.backable) {
        return
      }
      if (this.forceFallback) {
        const url = this.fallback
        if (url && url.startsWith('/pages/') && url.includes('/index')) {
          uni.reLaunch({ url })
          return
        }
      }
      safeBack(this.fallback)
    }
  }
}
</script>

<style scoped lang="scss">
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 24rpx;
  margin-bottom: 28rpx;
}

.left,
.right {
  width: 88rpx;
  min-height: 88rpx;
  display: flex;
  align-items: center;
}

.center {
  flex: 1;
  text-align: center;
}

.title {
  display: block;
  font-size: 30rpx;
  font-weight: 700;
  color: #f6f0e8;
}

.subtitle {
  display: block;
  margin-top: 6rpx;
  font-size: 20rpx;
  color: rgba(246, 240, 232, 0.45);
  letter-spacing: 4rpx;
  text-transform: uppercase;
}

.back-text {
  width: 72rpx;
  height: 72rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.08);
  color: #f6f0e8;
  font-size: 42rpx;
}
</style>
