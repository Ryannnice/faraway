<template>
  <view class="fab" @tap="goUpload">
    <view class="fab-inner">
      <view class="plus-ring">
        <text class="plus">+</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  methods: {
    goUpload() {
      uni.navigateTo({
        url: '/pages/upload/index'
      })
    }
  }
}
</script>

<style scoped lang="scss">
.fab {
  position: fixed;
  left: 50%;
  bottom: 18rpx;
  transform: translateX(-50%);
  z-index: 60;
  width: 198rpx;
  height: 198rpx;
  border-radius: 999rpx;
  background: radial-gradient(circle at center, rgba(255, 255, 255, 0.22) 0%, rgba(255, 255, 255, 0.08) 36%, rgba(255, 255, 255, 0) 72%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.fab-inner {
  width: 154rpx;
  height: 154rpx;
  border-radius: 999rpx;
  background: #ffffff;
  border: 8rpx solid #050505;
  box-shadow: 0 24rpx 70rpx rgba(0, 0, 0, 0.42);
  display: flex;
  align-items: center;
  justify-content: center;
}

.plus-ring {
  width: 94rpx;
  height: 94rpx;
  border-radius: 999rpx;
  border: 6rpx solid #101318;
  display: flex;
  align-items: center;
  justify-content: center;
}

.plus {
  color: #101318;
  font-size: 62rpx;
  font-weight: 700;
  line-height: 1;
}
</style>
