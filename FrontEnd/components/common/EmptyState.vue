<template>
  <view class="empty glass-card">
    <text class="empty-title">{{ title }}</text>
    <text class="empty-desc">{{ description }}</text>
  </view>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: '这里还没有内容'
    },
    description: {
      type: String,
      default: '等你来补上第一条记录。'
    }
  }
}
</script>

<style scoped lang="scss">
.empty {
  padding: 48rpx 36rpx;
  border-radius: 32rpx;
  text-align: center;
}

.empty-title {
  display: block;
  font-size: 30rpx;
  color: #f6f0e8;
  font-weight: 700;
}

.empty-desc {
  display: block;
  margin-top: 16rpx;
  font-size: 24rpx;
  color: rgba(246, 240, 232, 0.58);
  line-height: 1.7;
}
</style>
