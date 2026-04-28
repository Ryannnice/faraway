<template>
  <view class="page-shell">
    <AppHeader title="我的招募" subtitle="Recruitments" fallback="/pages/profile/index" />
    <view v-if="safeList.length" class="list-column">
      <view v-for="item in safeList" :key="item.id" class="recruit-card glass-card">
        <view class="recruit-head" @tap="toggleExpand(item.id)">
          <view>
            <text class="recruit-title">{{ item.destination }}</text>
            <text class="recruit-sub">{{ item.startDate }} · {{ item.days }} 天</text>
          </view>
          <view class="head-right">
            <text class="count-chip">{{ item.applicationCount }} 条申请</text>
            <text class="expand-arrow">{{ expandedId === item.id ? '−' : '+' }}</text>
          </view>
        </view>

        <view v-if="expandedId === item.id" class="application-section">
          <view v-if="getApplications(item).length" class="application-list">
            <view v-for="apply in getApplications(item)" :key="apply.applicationId" class="application-card">
              <view class="application-top">
                <view class="user-row" @tap="openUser(apply.applicantUserId)">
                  <image class="user-avatar" :src="apply.applicantAvatar" mode="aspectFill" />
                  <view class="user-text">
                    <text class="user-name">{{ apply.applicantNickname }}</text>
                    <text class="user-sub">点击查看主页</text>
                  </view>
                </view>
                <text class="status-chip" :class="apply.status">{{ getStatusText(apply.status) }}</text>
              </view>

              <view class="meta-row">
                <text>{{ apply.destination }}</text>
                <text>{{ apply.startDate }}</text>
                <text>{{ apply.days }} 天</text>
              </view>

              <view class="action-row">
                <view class="pill-button secondary-btn" :class="{ disabled: apply.status !== 'pending' }" @tap="reject(item.id, apply)">
                  拒绝
                </view>
                <view class="primary-button half-btn" :class="{ disabled: apply.status !== 'pending' }" @tap="approve(item.id, apply)">
                  同意
                </view>
              </view>
            </view>
          </view>
          <EmptyState v-else title="暂时还没有申请" description="发布后别人申请你的招募，会显示在这里。" />
        </view>
      </view>
    </view>
    <EmptyState v-else title="你还没有发布招募" description="去找搭子页填写条件后，点右上角发布即可出现在这里。" />
  </view>
</template>

<script>
import AppHeader from '../../components/common/AppHeader.vue'
import EmptyState from '../../components/common/EmptyState.vue'
import { approveRecruitmentApplication, getMyRecruitments, rejectRecruitmentApplication } from '../../api/modules/match'
import { MATCH_APPLICATION_STATUS } from '../../constants/enums'
import { go } from '../../utils/navigation'

export default {
  components: {
    AppHeader,
    EmptyState
  },
  data() {
    return {
      list: [],
      expandedId: null
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
    getStatusText(status) {
      return MATCH_APPLICATION_STATUS[status] || status
    },
    async loadData() {
      const result = await getMyRecruitments()
      this.list = Array.isArray(result && result.list) ? result.list : []
      if (this.expandedId && !this.list.find((item) => item.id === this.expandedId)) {
        this.expandedId = null
      }
    },
    getApplications(item) {
      return Array.isArray(item && item.applications) ? item.applications : []
    },
    toggleExpand(id) {
      this.expandedId = this.expandedId === id ? null : id
    },
    openUser(userId) {
      go(`/pages/user-profile/index?userId=${userId}`)
    },
    async approve(recruitId, apply) {
      if (apply.status !== 'pending') {
        return
      }
      await approveRecruitmentApplication(recruitId, apply.applicationId)
      await this.loadData()
    },
    async reject(recruitId, apply) {
      if (apply.status !== 'pending') {
        return
      }
      await rejectRecruitmentApplication(recruitId, apply.applicationId)
      await this.loadData()
    }
  }
}
</script>

<style scoped lang="scss">
.list-column,
.application-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.recruit-card {
  padding: 28rpx;
  border-radius: 30rpx;
}

.recruit-head,
.head-right,
.application-top,
.user-row,
.action-row,
.meta-row {
  display: flex;
  align-items: center;
}

.recruit-head,
.application-top {
  justify-content: space-between;
}

.recruit-title,
.user-name {
  display: block;
  font-size: 30rpx;
  font-weight: 700;
}

.recruit-sub,
.user-sub {
  display: block;
  margin-top: 10rpx;
  font-size: 22rpx;
  color: rgba(246, 240, 232, 0.5);
}

.head-right {
  gap: 16rpx;
}

.count-chip {
  min-height: 56rpx;
  padding: 0 20rpx;
  border-radius: 999rpx;
  background: rgba(236, 214, 179, 0.12);
  display: flex;
  align-items: center;
  color: #ecd6b3;
  font-size: 22rpx;
}

.expand-arrow {
  font-size: 36rpx;
  color: rgba(246, 240, 232, 0.72);
}

.application-section {
  margin-top: 24rpx;
}

.application-card {
  padding: 22rpx;
  border-radius: 24rpx;
  background: rgba(255, 255, 255, 0.04);
}

.user-avatar {
  width: 74rpx;
  height: 74rpx;
  border-radius: 50%;
}

.user-text {
  margin-left: 16rpx;
}

.status-chip {
  min-width: 112rpx;
  height: 52rpx;
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

.meta-row {
  gap: 18rpx;
  margin-top: 18rpx;
  flex-wrap: wrap;
  font-size: 24rpx;
  color: rgba(246, 240, 232, 0.74);
}

.action-row {
  gap: 16rpx;
  margin-top: 20rpx;
}

.secondary-btn,
.half-btn {
  flex: 1;
}

.disabled {
  opacity: 0.68;
}
</style>
