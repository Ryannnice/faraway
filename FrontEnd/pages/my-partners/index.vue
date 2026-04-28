<template>
  <view class="partner-page">
    <view class="hero-shell">
      <view class="hero-header">
        <view class="back-button" @tap="goBack">‹</view>
        <view class="hero-title-group">
          <text class="hero-kicker">PARTNER HUB</text>
          <text class="hero-title">我的搭子</text>
        </view>
        <view class="hero-spacer" />
      </view>
    </view>

    <view class="panel-shell">
      <view v-if="hasRealtimeRecord" class="realtime-card" @tap="openRealtimePage">
        <view class="card-top">
          <view class="card-copy">
            <text class="card-kicker">实时找搭子</text>
            <text class="card-title">{{ buildRealtimeTitle() }}</text>
            <text class="card-subline">{{ buildRealtimeSubtitle() }}</text>
          </view>
          <view class="status-badge" :class="realtimeBadgeClass">
            <text>{{ realtimeStatusText }}</text>
          </view>
        </view>

        <view class="info-grid">
          <view class="info-block">
            <text class="info-label">日期范围</text>
            <text class="info-value">{{ formatTravelRange(realtimeState) }}</text>
          </view>
          <view class="info-block">
            <text class="info-label">状态说明</text>
            <text class="info-value">{{ buildRealtimeHint() }}</text>
          </view>
          <view class="info-block">
            <text class="info-label">搭子对象</text>
            <text class="info-value">{{ buildRealtimePeer() }}</text>
          </view>
          <view class="info-block">
            <text class="info-label">入口</text>
            <text class="info-value">点击查看详情</text>
          </view>
        </view>
      </view>

      <view class="tab-row">
        <view class="partner-tab" :class="{ active: activeTab === 'recruitments' }" @tap="switchTab('recruitments')">
          <text class="tab-icon">◎</text>
          <text class="tab-label">我的招募帖</text>
        </view>
        <view class="partner-tab" :class="{ active: activeTab === 'applications' }" @tap="switchTab('applications')">
          <text class="tab-icon">✈</text>
          <text class="tab-label">我的联系记录</text>
        </view>
      </view>

      <view v-if="activeTab === 'recruitments'" class="content-section">
        <view v-if="safeRecruitments.length" class="partner-list">
          <view v-for="item in safeRecruitments" :key="item.id" class="partner-card">
            <view class="card-top">
              <view class="card-copy">
                <text class="card-kicker">我的招募帖</text>
                <text class="card-title">{{ buildRecruitmentTitle(item) }}</text>
                <text class="card-subline">收到申请：{{ item.applicationCount }} 人</text>
              </view>
              <view class="status-badge" :class="item.status">
                <text>{{ getRecruitmentStatusText(item.status) }}</text>
              </view>
            </view>

            <view class="info-grid">
              <view class="info-block">
                <text class="info-label">出发时间</text>
                <text class="info-value">{{ formatDate(item.startDate) }}</text>
              </view>
              <view class="info-block">
                <text class="info-label">停留天数</text>
                <text class="info-value">{{ item.days }} 天</text>
              </view>
              <view class="info-block">
                <text class="info-label">状态</text>
                <text class="info-value">{{ getRecruitmentStatusText(item.status) }}</text>
              </view>
              <view class="info-block">
                <text class="info-label">申请人数</text>
                <text class="info-value">{{ item.applicationCount }} 人</text>
              </view>
            </view>

            <view v-if="getApplications(item).length" class="sub-records">
              <view v-for="apply in getApplications(item)" :key="apply.applicationId" class="sub-record">
                <view class="sub-record-top">
                  <view class="user-row" @tap="openUser(apply.applicantUserId)">
                    <image class="user-avatar" :src="apply.applicantAvatar" mode="aspectFill" />
                    <view class="user-meta">
                      <text class="user-name">{{ apply.applicantNickname }}</text>
                      <text class="user-sub">查看主页</text>
                    </view>
                  </view>
                  <text class="record-chip" :class="apply.status">{{ getStatusText(apply.status) }}</text>
                </view>
                <view class="sub-record-actions">
                  <view class="ghost-action" :class="{ disabled: apply.status !== 'pending' }" @tap="reject(item.id, apply)">拒绝</view>
                  <view class="solid-action" :class="{ disabled: apply.status !== 'pending' }" @tap="approve(item.id, apply)">同意</view>
                </view>
              </view>
            </view>
          </view>
        </view>

        <view v-else class="empty-shell">
          <view class="empty-icon">◎</view>
          <text class="empty-title">{{ hasRealtimeRecord ? '当前实时找搭子记录展示在上方' : '你还没有发布招募帖' }}</text>
          <text class="empty-desc">{{ hasRealtimeRecord ? '实时匹配不会进入旧招募帖列表，但你可以点上方卡片继续查看。' : '先去招募搭子，公开你的目的地、时间和偏好。' }}</text>
        </view>
      </view>

      <view v-else class="content-section">
        <view v-if="safeApplications.length" class="partner-list">
          <view v-for="item in safeApplications" :key="item.applicationId" class="partner-card">
            <view class="card-top">
              <view class="card-copy">
                <text class="card-kicker">目标招募帖</text>
                <text class="card-title">{{ buildApplicationTitle(item) }}</text>
                <text class="card-subline">联系对象：{{ item.publisherNickname }}</text>
              </view>
              <view class="status-badge compact" :class="item.status">
                <text>{{ getStatusText(item.status) }}</text>
              </view>
            </view>

            <view class="contact-row" @tap="openUser(item.publisherUserId)">
              <image class="user-avatar" :src="item.publisherAvatar" mode="aspectFill" />
              <view class="user-meta">
                <text class="user-name">{{ item.publisherNickname }}</text>
                <text class="user-sub">点击查看主页</text>
              </view>
            </view>

            <view class="info-grid">
              <view class="info-block">
                <text class="info-label">出发时间</text>
                <text class="info-value">{{ formatDate(item.startDate) }}</text>
              </view>
              <view class="info-block">
                <text class="info-label">停留天数</text>
                <text class="info-value">{{ item.days }} 天</text>
              </view>
              <view class="info-block">
                <text class="info-label">联系状态</text>
                <text class="info-value">{{ getStatusText(item.status) }}</text>
              </view>
              <view class="info-block">
                <text class="info-label">目的地</text>
                <text class="info-value">{{ item.destination || '待确认' }}</text>
              </view>
            </view>
          </view>
        </view>

        <view v-else class="empty-shell">
          <view class="empty-icon send">✈</view>
          <text class="empty-title">你还没有联系记录</text>
          <text class="empty-desc">去找搭子页匹配合适的人，发起联系后会显示在这里。</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { approveRecruitmentApplication, getCurrentRealtimeMatch, getMyMatchApplications, getMyRecruitments, rejectRecruitmentApplication } from '../../api/modules/match'
import { MATCH_APPLICATION_STATUS, MATCH_RECRUITMENT_STATUS } from '../../constants/enums'
import { go, safeBack } from '../../utils/navigation'

export default {
  data() {
    return {
      activeTab: 'recruitments',
      recruitments: [],
      applications: [],
      realtimeState: null
    }
  },
  computed: {
    safeRecruitments() {
      return Array.isArray(this.recruitments) ? this.recruitments : []
    },
    safeApplications() {
      return Array.isArray(this.applications) ? this.applications : []
    },
    hasRealtimeRecord() {
      return !!(this.realtimeState && this.realtimeState.request_id)
    },
    realtimeStatusText() {
      const status = this.realtimeState && this.realtimeState.status
      const labelMap = {
        pending: '匹配中',
        matched_waiting_decision: '待决定',
        matched_accepted: '已确认',
        failed: '未匹配到',
        cancelled: '已取消',
        finished: '已结束'
      }
      return labelMap[status] || '实时找搭子'
    },
    realtimeBadgeClass() {
      const status = this.realtimeState && this.realtimeState.status
      if (status === 'matched_accepted') {
        return 'approved'
      }
      if (status === 'failed' || status === 'cancelled') {
        return 'rejected'
      }
      return 'pending'
    }
  },
  onLoad(options) {
    const tab = options && options.tab
    if (tab === 'applications' || tab === 'recruitments') {
      this.activeTab = tab
    }
  },
  onShow() {
    this.loadData()
  },
  methods: {
    async loadData() {
      const [recruitmentResult, applicationResult, realtimeResult] = await Promise.all([
        getMyRecruitments(),
        getMyMatchApplications(),
        getCurrentRealtimeMatch()
      ])
      this.recruitments = Array.isArray(recruitmentResult && recruitmentResult.list) ? recruitmentResult.list : []
      this.applications = Array.isArray(applicationResult && applicationResult.list) ? applicationResult.list : []
      this.realtimeState = realtimeResult && realtimeResult.request_id ? realtimeResult : null
    },
    switchTab(tab) {
      this.activeTab = tab
    },
    goBack() {
      safeBack('/pages/profile/index')
    },
    openUser(userId) {
      go(`/pages/user-profile/index?userId=${userId}`)
    },
    openRealtimePage() {
      go('/pages/match/index')
    },
    getApplications(item) {
      return Array.isArray(item && item.applications) ? item.applications : []
    },
    getStatusText(status) {
      return MATCH_APPLICATION_STATUS[status] || status
    },
    getRecruitmentStatusText(status) {
      return MATCH_RECRUITMENT_STATUS[status] || '招募中'
    },
    buildRecruitmentTitle(item) {
      return item && item.destination ? `去${item.destination}找搭子` : '我的招募帖'
    },
    buildApplicationTitle(item) {
      return item && item.destination ? `关于 ${item.destination} 的联系记录` : '我的联系记录'
    },
    buildRealtimeTitle() {
      const destination = this.realtimeState && this.realtimeState.destination
      return destination ? `去${destination}的实时找搭子` : '当前实时找搭子'
    },
    buildRealtimeSubtitle() {
      if (!this.realtimeState) {
        return '点击查看详情'
      }
      if (this.realtimeState.status === 'matched_accepted' && this.realtimeState.pair) {
        return `已与 ${this.realtimeState.pair.peer_nickname || '搭子'} 确认见面`
      }
      if (this.realtimeState.status === 'matched_waiting_decision' && this.realtimeState.candidate) {
        return `当前候选：${this.realtimeState.candidate.peer_nickname || '待确认'}`
      }
      return '点击查看当前实时匹配状态'
    },
    buildRealtimeHint() {
      if (!this.realtimeState) {
        return '待查看'
      }
      if (this.realtimeState.status === 'matched_accepted' && this.realtimeState.pair) {
        return this.formatDateTime(this.realtimeState.pair.meet_time)
      }
      if (this.realtimeState.status === 'matched_waiting_decision' && this.realtimeState.candidate) {
        return `截止 ${this.formatDateTime(this.realtimeState.candidate.decision_expires_at)}`
      }
      if (this.realtimeState.match_deadline_at) {
        return `截止 ${this.formatDateTime(this.realtimeState.match_deadline_at)}`
      }
      return this.realtimeStatusText
    },
    buildRealtimePeer() {
      if (!this.realtimeState) {
        return '待匹配'
      }
      if (this.realtimeState.pair && this.realtimeState.pair.peer_nickname) {
        return this.realtimeState.pair.peer_nickname
      }
      if (this.realtimeState.candidate && this.realtimeState.candidate.peer_nickname) {
        return this.realtimeState.candidate.peer_nickname
      }
      return '待匹配'
    },
    formatTravelRange(item) {
      if (!item) {
        return '待确定'
      }
      return `${this.formatDate(item.travel_start_date)} - ${this.formatDate(item.travel_end_date)}`
    },
    formatDate(value) {
      if (!value) {
        return '待确定'
      }
      const parts = String(value).split('-')
      if (parts.length === 3) {
        return `${Number(parts[0])}年${Number(parts[1])}月${Number(parts[2])}日`
      }
      return value
    },
    formatDateTime(value) {
      if (!value) {
        return '待确定'
      }
      const [datePart, timePart = ''] = String(value).split('T')
      return `${this.formatDate(datePart)} ${timePart.slice(0, 5)}`
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
.partner-page {
  min-height: 100vh;
  background: #000;
  color: #fff;
}

.hero-shell {
  padding: 28rpx 40rpx 30rpx;
  border-bottom: 1rpx solid rgba(255, 255, 255, 0.06);
}

.hero-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 18rpx;
}

.back-button,
.hero-spacer {
  width: 72rpx;
  height: 72rpx;
}

.back-button {
  border-radius: 999rpx;
  border: 1rpx solid rgba(255, 255, 255, 0.08);
  background: rgba(255, 255, 255, 0.06);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 44rpx;
  color: #f5f5f5;
}

.hero-title-group {
  flex: 1;
  text-align: center;
}

.hero-kicker {
  display: block;
  font-size: 18rpx;
  letter-spacing: 8rpx;
  color: rgba(255, 255, 255, 0.3);
}

.hero-title {
  display: block;
  margin-top: 14rpx;
  font-size: 58rpx;
  font-weight: 700;
  letter-spacing: 4rpx;
}

.panel-shell {
  padding: 34rpx 32rpx 120rpx;
}

.realtime-card {
  margin-bottom: 22rpx;
  padding: 28rpx;
  border-radius: 30rpx;
  background: linear-gradient(135deg, rgba(38, 57, 88, 0.96) 0%, rgba(16, 24, 38, 0.98) 100%);
  border: 1rpx solid rgba(255, 255, 255, 0.08);
}

.tab-row {
  display: flex;
  gap: 20rpx;
}

.partner-tab {
  flex: 1;
  min-height: 88rpx;
  padding: 0 24rpx;
  border-radius: 999rpx;
  border: 1rpx solid rgba(255, 255, 255, 0.08);
  background: #121212;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12rpx;
  color: rgba(255, 255, 255, 0.45);
}

.partner-tab.active {
  background: #fff;
  color: #060606;
}

.tab-icon {
  font-size: 28rpx;
}

.tab-label {
  font-size: 28rpx;
  font-weight: 700;
}

.content-section {
  margin-top: 34rpx;
}

.partner-list,
.sub-records {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.partner-card {
  padding: 30rpx;
  border-radius: 36rpx;
  background: #111;
  border: 1rpx solid rgba(255, 255, 255, 0.06);
}

.card-top,
.sub-record-top,
.user-row,
.contact-row,
.sub-record-actions {
  display: flex;
  align-items: center;
}

.card-top,
.sub-record-top {
  justify-content: space-between;
}

.card-copy {
  flex: 1;
  min-width: 0;
  padding-right: 24rpx;
}

.card-kicker,
.info-label,
.user-sub {
  display: block;
  font-size: 22rpx;
  color: rgba(255, 255, 255, 0.34);
}

.card-title {
  display: block;
  margin-top: 18rpx;
  font-size: 54rpx;
  line-height: 1.12;
  font-weight: 800;
}

.card-subline {
  display: block;
  margin-top: 18rpx;
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.5);
}

.status-badge {
  min-width: 132rpx;
  min-height: 132rpx;
  border-radius: 36rpx;
  padding: 18rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-size: 24rpx;
  font-weight: 700;
}

.status-badge.compact {
  min-width: 120rpx;
  min-height: 120rpx;
}

.status-badge.open,
.status-badge.pending {
  background: rgba(17, 132, 98, 0.42);
  color: #6effcf;
}

.status-badge.closed {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.65);
}

.status-badge.approved {
  background: rgba(17, 132, 98, 0.42);
  color: #6effcf;
}

.status-badge.rejected {
  background: rgba(113, 113, 113, 0.28);
  color: rgba(255, 255, 255, 0.72);
}

.contact-row {
  margin-top: 26rpx;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20rpx;
  margin-top: 26rpx;
}

.info-block {
  min-height: 150rpx;
  padding: 24rpx;
  border-radius: 26rpx;
  background: #171717;
  border: 1rpx solid rgba(255, 255, 255, 0.05);
  box-sizing: border-box;
}

.info-value,
.user-name {
  display: block;
  color: #fff;
}

.info-value {
  margin-top: 28rpx;
  font-size: 28rpx;
  font-weight: 700;
  line-height: 1.3;
}

.sub-record {
  padding: 22rpx;
  border-radius: 28rpx;
  background: #171717;
  border: 1rpx solid rgba(255, 255, 255, 0.05);
}

.user-avatar {
  width: 76rpx;
  height: 76rpx;
  border-radius: 999rpx;
}

.user-meta {
  margin-left: 16rpx;
}

.user-name {
  font-size: 28rpx;
  font-weight: 700;
}

.user-sub {
  margin-top: 8rpx;
}

.record-chip {
  min-width: 112rpx;
  height: 52rpx;
  padding: 0 18rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22rpx;
  font-weight: 700;
}

.record-chip.pending {
  background: rgba(236, 214, 179, 0.12);
  color: #ecd6b3;
}

.record-chip.approved {
  background: rgba(108, 214, 167, 0.14);
  color: #6cd6a7;
}

.record-chip.rejected {
  background: rgba(255, 141, 122, 0.14);
  color: #ff8d7a;
}

.sub-record-actions {
  gap: 16rpx;
  margin-top: 20rpx;
}

.ghost-action,
.solid-action {
  flex: 1;
  height: 82rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26rpx;
  font-weight: 700;
}

.ghost-action {
  background: rgba(255, 255, 255, 0.06);
  border: 1rpx solid rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.82);
}

.solid-action {
  background: #fff;
  color: #050505;
}

.ghost-action.disabled,
.solid-action.disabled {
  opacity: 0.46;
}

.empty-shell {
  min-height: 900rpx;
  padding: 160rpx 40rpx 0;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.empty-icon {
  width: 132rpx;
  height: 132rpx;
  border-radius: 999rpx;
  border: 1rpx solid rgba(255, 255, 255, 0.08);
  background: #121212;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 50rpx;
  color: rgba(255, 255, 255, 0.3);
}

.empty-icon.send {
  font-size: 42rpx;
}

.empty-title {
  margin-top: 52rpx;
  font-size: 44rpx;
  font-weight: 800;
  line-height: 1.2;
}

.empty-desc {
  margin-top: 20rpx;
  font-size: 28rpx;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.42);
}
</style>
