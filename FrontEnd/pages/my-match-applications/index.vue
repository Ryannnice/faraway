<template>
  <view class="page-shell">
    <AppHeader title="我的申请记录" subtitle="Applications" fallback="/pages/profile/index" />
    <view v-if="safeList.length" class="list-column">
      <view v-for="item in safeList" :key="item.applicationId" class="record-card glass-card">
        <view class="record-top">
          <view class="user-row" @tap="openUser(item.publisherUserId)">
            <image class="user-avatar" :src="item.publisherAvatar" mode="aspectFill" />
            <view class="user-text">
              <text class="user-name">{{ item.publisherNickname }}</text>
              <text class="user-sub">点击查看主页</text>
            </view>
          </view>
          <text class="status-chip" :class="item.status">{{ getStatusText(item.status) }}</text>
        </view>

        <view class="meta-grid">
          <view class="meta-item">
            <text class="meta-label">目的地</text>
            <text class="meta-value">{{ item.destination }}</text>
          </view>
          <view class="meta-item">
            <text class="meta-label">出发日期</text>
            <text class="meta-value">{{ item.startDate }}</text>
          </view>
          <view class="meta-item">
            <text class="meta-label">停留天数</text>
            <text class="meta-value">{{ item.days }} 天</text>
          </view>
        </view>
      </view>
    </view>
    <EmptyState v-else title="你还没有申请记录" description="去找搭子页匹配合适的人，点申请后会显示在这里。" />
  </view>
</template>

<script>
import AppHeader from '../../components/common/AppHeader.vue'
import EmptyState from '../../components/common/EmptyState.vue'
import { getMyMatchApplications } from '../../api/modules/match'
import { MATCH_APPLICATION_STATUS } from '../../constants/enums'
import { go } from '../../utils/navigation'

export default {
  components: {
    AppHeader,
    EmptyState
  },
  data() {
    return {
      list: []
    }
  },
  computed: {
    safeList() {
      return Array.isArray(this.list) ? this.list : []
    }
  },
  onShow() {
    this.loadData()
  },
  methods: {
    async loadData() {
      const result = await getMyMatchApplications()
      this.list = Array.isArray(result && result.list) ? result.list : []
    },
    getStatusText(status) {
      return MATCH_APPLICATION_STATUS[status] || status
    },
    openUser(userId) {
      go(`/pages/user-profile/index?userId=${userId}`)
    }
  }
}
</script>

<style scoped lang="scss">
.list-column {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.record-card {
  padding: 28rpx;
  border-radius: 30rpx;
}

.record-top,
.user-row {
  display: flex;
  align-items: center;
}

.record-top {
  justify-content: space-between;
}

.user-avatar {
  width: 78rpx;
  height: 78rpx;
  border-radius: 50%;
}

.user-text {
  margin-left: 16rpx;
}

.user-name,
.meta-value {
  display: block;
}

.user-name {
  font-size: 30rpx;
  font-weight: 700;
}

.user-sub,
.meta-label {
  display: block;
  margin-top: 8rpx;
  font-size: 22rpx;
  color: rgba(246, 240, 232, 0.48);
}

.status-chip {
  min-width: 120rpx;
  height: 56rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22rpx;
  font-weight: 700;
}

.status-chip.pending {
  background: rgba(236, 214, 179, 0.12);
  color: #ecd6b3;
}

.status-chip.approved {
  background: rgba(108, 214, 167, 0.14);
  color: #6cd6a7;
}

.status-chip.rejected {
  background: rgba(255, 141, 122, 0.14);
  color: #ff8d7a;
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18rpx;
  margin-top: 24rpx;
}

.meta-item {
  padding: 18rpx;
  border-radius: 22rpx;
  background: rgba(255, 255, 255, 0.04);
}

.meta-value {
  margin-top: 10rpx;
  font-size: 28rpx;
  font-weight: 700;
}
</style>
