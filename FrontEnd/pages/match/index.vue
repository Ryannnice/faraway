<template>
  <view class="page-shell">
    <AppHeader title="找搭子" subtitle="Match" fallback="/pages/home/index">
      <view class="publish-entry" @tap="publishRecruitment">发布</view>
    </AppHeader>

    <view class="form-stack">
      <view class="field glass-card">
        <text class="field-label">目的地</text>
        <input v-model="form.destination" class="field-input" placeholder="冰岛、大理..." placeholder-style="color: rgba(246,240,232,0.24)" />
      </view>
      <view class="field glass-card">
        <text class="field-label">出发日期</text>
        <input v-model="form.startDate" class="field-input" placeholder="2026-05-01" placeholder-style="color: rgba(246,240,232,0.24)" />
      </view>
      <view class="field glass-card">
        <text class="field-label">停留天数</text>
        <input v-model="form.days" class="field-input" placeholder="3" placeholder-style="color: rgba(246,240,232,0.24)" />
      </view>
      <button class="primary-button" @tap="submit">开始匹配</button>
    </view>

    <view v-if="hasSearched" class="result-block">
      <view class="result-head">
        <text class="section-kicker">Recommended</text>
        <text class="result-count">共 {{ safeList.length }} 条</text>
      </view>
      <view v-if="safeList.length" class="list-column">
        <view v-for="item in safeList" :key="item.recruitId" class="match-card glass-card">
          <view class="card-top">
            <view class="user-row" @tap="openUser(item.publisherUserId)">
              <image class="user-avatar" :src="item.publisherAvatar" mode="aspectFill" />
              <view class="user-text">
                <text class="user-name">{{ item.publisherNickname }}</text>
                <text class="user-sub">查看主页</text>
              </view>
            </view>
            <view class="status-chip" :class="item.applicationStatus">{{ getStatusText(item.applicationStatus) }}</view>
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

          <view class="card-actions">
            <view class="pill-button secondary-btn" @tap="openUser(item.publisherUserId)">看主页</view>
            <view class="primary-button apply-btn" :class="{ disabled: item.applicationStatus !== 'none' }" @tap="apply(item)">
              {{ getStatusText(item.applicationStatus) }}
            </view>
          </view>
        </view>
      </view>
      <EmptyState v-else title="暂时没有更合适的搭子" description="可以修改条件重新匹配，或者直接发布你的招募。" />
    </view>
  </view>
</template>

<script>
import AppHeader from '../../components/common/AppHeader.vue'
import EmptyState from '../../components/common/EmptyState.vue'
import { applyRecruitment, createRecruitment, getMatchRecommendations } from '../../api/modules/match'
import { MATCH_APPLICATION_STATUS } from '../../constants/enums'
import { go } from '../../utils/navigation'

export default {
  components: {
    AppHeader,
    EmptyState
  },
  data() {
    return {
      form: {
        destination: '',
        startDate: '',
        days: '3'
      },
      list: [],
      hasSearched: false
    }
  },
  computed: {
    safeList() {
      return Array.isArray(this.list) ? this.list : []
    }
  },
  methods: {
    validateForm() {
      return this.form.destination && this.form.startDate && this.form.days
    },
    getStatusText(status) {
      return MATCH_APPLICATION_STATUS[status] || '申请'
    },
    async submit() {
      if (!this.validateForm()) {
        uni.showToast({
          title: '请先填写完整信息',
          icon: 'none'
        })
        return
      }
      const result = await getMatchRecommendations(this.form)
      this.list = Array.isArray(result && result.list) ? result.list : []
      this.hasSearched = true
    },
    async publishRecruitment() {
      if (!this.validateForm()) {
        uni.showToast({
          title: '请先填写完整信息',
          icon: 'none'
        })
        return
      }
      await createRecruitment(this.form)
      uni.showToast({
        title: '已发布',
        icon: 'none'
      })
      setTimeout(() => {
        go('/pages/my-partners/index?tab=recruitments')
      }, 240)
    },
    async apply(item) {
      if (item.applicationStatus !== 'none') {
        return
      }
      const result = await applyRecruitment(item.recruitId)
      item.applicationStatus = result.status
      uni.showToast({
        title: '申请已发出',
        icon: 'none'
      })
    },
    openUser(userId) {
      go(`/pages/user-profile/index?userId=${userId}`)
    }
  }
}
</script>

<style scoped lang="scss">
.publish-entry {
  min-width: 96rpx;
  min-height: 64rpx;
  border-radius: 999rpx;
  padding: 0 18rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.08);
  font-size: 22rpx;
  color: #ecd6b3;
}

.form-stack,
.list-column {
  display: flex;
  flex-direction: column;
  gap: 22rpx;
}

.field,
.match-card {
  padding: 26rpx 28rpx;
  border-radius: 28rpx;
}

.field-label,
.meta-label,
.user-sub {
  display: block;
  font-size: 22rpx;
  letter-spacing: 4rpx;
  color: rgba(246, 240, 232, 0.46);
}

.field-input {
  margin-top: 16rpx;
  font-size: 34rpx;
  color: #f6f0e8;
}

.result-block {
  margin-top: 34rpx;
}

.result-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20rpx;
}

.result-count {
  font-size: 22rpx;
  color: rgba(246, 240, 232, 0.52);
}

.card-top,
.user-row,
.card-actions {
  display: flex;
  align-items: center;
}

.card-top,
.card-actions {
  justify-content: space-between;
}

.user-avatar {
  width: 86rpx;
  height: 86rpx;
  border-radius: 50%;
}

.user-text {
  margin-left: 18rpx;
}

.user-name,
.meta-value {
  display: block;
  color: #f6f0e8;
}

.user-name {
  font-size: 30rpx;
  font-weight: 700;
}

.user-sub {
  margin-top: 8rpx;
  letter-spacing: 0;
}

.status-chip {
  min-width: 120rpx;
  height: 56rpx;
  padding: 0 18rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22rpx;
  font-weight: 700;
}

.status-chip.none,
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
  margin-top: 26rpx;
}

.meta-item {
  padding: 18rpx;
  border-radius: 22rpx;
  background: rgba(255, 255, 255, 0.04);
}

.meta-value {
  margin-top: 12rpx;
  font-size: 28rpx;
  font-weight: 700;
}

.card-actions {
  gap: 18rpx;
  margin-top: 24rpx;
}

.secondary-btn,
.apply-btn {
  flex: 1;
}

.apply-btn.disabled {
  opacity: 0.72;
}
</style>
