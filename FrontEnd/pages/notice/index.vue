<template>
  <view class="page-shell">
    <AppHeader title="通知" subtitle="Notice" fallback="/pages/profile/index" />
    <view class="list-column">
      <view v-for="item in list" :key="item.id" class="notice-card glass-card">
        <text class="notice-type">{{ item.type }}</text>
        <text class="notice-title">{{ item.title }}</text>
        <text class="notice-time">{{ item.createdAt }}</text>
      </view>
    </view>
  </view>
</template>

<script>
import AppHeader from '../../components/common/AppHeader.vue'
import { getMyNotifications } from '../../api/modules/user'

export default {
  components: {
    AppHeader
  },
  data() {
    return {
      list: []
    }
  },
  onShow() {
    this.loadData()
  },
  methods: {
    async loadData() {
      const result = await getMyNotifications()
      this.list = result.list || []
    }
  }
}
</script>

<style scoped lang="scss">
.list-column {
  display: flex;
  flex-direction: column;
  gap: 18rpx;
}

.notice-card {
  padding: 26rpx;
  border-radius: 28rpx;
}

.notice-type,
.notice-time {
  display: block;
  font-size: 22rpx;
  color: rgba(246, 240, 232, 0.48);
}

.notice-title {
  display: block;
  margin-top: 10rpx;
  font-size: 28rpx;
  line-height: 1.6;
}

.notice-time {
  margin-top: 14rpx;
}
</style>
