<template>
  <view class="page-shell">
    <AppHeader title="找搭子" subtitle="Realtime Match" fallback="/pages/home/index">
      <view class="record-entry" @tap="openRecords">记录</view>
    </AppHeader>

    <view class="hero-card glass-card">
      <text class="section-kicker">Match Now</text>
      <text class="hero-title">填完条件，系统会替你持续找人</text>
      <text class="hero-desc">只要地点一致、日期有重叠，就会按偏好相似度优先推荐给你。</text>
    </view>

    <view v-if="currentView === 'form'" class="panel-stack">
      <view class="field-card glass-card">
        <text class="field-label">目的地</text>
        <input
          v-model="form.destination"
          class="field-input"
          placeholder="例如：大阪、大理、冰岛"
          placeholder-style="color: rgba(246,240,232,0.24)"
        />
      </view>

      <view class="two-field-row">
        <view class="field-card glass-card field-half">
          <text class="field-label">开始日期</text>
          <input
            v-model="form.travel_start_date"
            class="field-input"
            placeholder="2026-05-01"
            placeholder-style="color: rgba(246,240,232,0.24)"
          />
        </view>
        <view class="field-card glass-card field-half">
          <text class="field-label">结束日期</text>
          <input
            v-model="form.travel_end_date"
            class="field-input"
            placeholder="2026-05-04"
            placeholder-style="color: rgba(246,240,232,0.24)"
          />
        </view>
      </view>

      <view class="field-card glass-card">
        <text class="field-label">旅行偏好</text>
        <view class="tag-grid">
          <view
            v-for="tag in preferenceTagOptions"
            :key="tag"
            class="tag-option"
            :class="{ active: hasTag(tag) }"
            @tap="toggleTag(tag)"
          >
            {{ tag }}
          </view>
        </view>
      </view>

      <view class="field-card glass-card">
        <text class="field-label">补充说明</text>
        <textarea
          v-model="form.preference_text"
          class="field-textarea"
          maxlength="200"
          placeholder="例如：喜欢白天走路拍照，不太能熬夜，愿意一起吃当地小店。"
          placeholder-style="color: rgba(246,240,232,0.24)"
        />
      </view>

      <view v-if="state.status === 'pending'" class="hint-card glass-card">
        <text>提交后会替换当前正在匹配中的条件。</text>
      </view>

      <button class="primary-button submit-button" :class="{ disabled: busy }" @tap="submitRealtimeMatch">
        {{ submitButtonText }}
      </button>

      <view v-if="canReturnToPending" class="secondary-action" @tap="cancelEdit">返回当前匹配</view>
    </view>

    <view v-else-if="currentView === 'pending'" class="panel-stack">
      <view class="status-card glass-card">
        <text class="section-kicker">Pending</text>
        <text class="state-title">系统正在寻找更合适的搭子</text>
        <text class="state-desc">页面会自动刷新，一旦出现候选对象就切到待决定状态。</text>
      </view>

      <view class="summary-card glass-card">
        <view class="summary-grid">
          <view class="summary-item">
            <text class="summary-label">目的地</text>
            <text class="summary-value">{{ state.destination || '待填写' }}</text>
          </view>
          <view class="summary-item">
            <text class="summary-label">出发日期</text>
            <text class="summary-value">{{ formatDate(state.travel_start_date) }}</text>
          </view>
          <view class="summary-item">
            <text class="summary-label">结束日期</text>
            <text class="summary-value">{{ formatDate(state.travel_end_date) }}</text>
          </view>
          <view class="summary-item">
            <text class="summary-label">匹配截止</text>
            <text class="summary-value">{{ formatDateTime(state.match_deadline_at) }}</text>
          </view>
        </view>
        <view v-if="stateTags.length" class="chips-row">
          <text v-for="tag in stateTags" :key="tag" class="tag-badge">{{ tag }}</text>
        </view>
        <text v-if="state.preference_text" class="note-text">{{ state.preference_text }}</text>
      </view>

      <view class="action-row">
        <view class="secondary-action action-half" @tap="beginEdit">重新填写条件</view>
        <view class="danger-action action-half" :class="{ disabled: busy }" @tap="cancelPendingMatch">取消匹配</view>
      </view>
    </view>

    <view v-else-if="currentView === 'waiting'" class="panel-stack">
      <view class="status-card glass-card">
        <text class="section-kicker">Candidate</text>
        <text class="state-title">系统为你找到了一位候选搭子</text>
        <text class="state-desc">
          {{ hasAcceptedCandidate ? '你已经同意，正在等待对方回应。' : '你们的信息已经有较高重合度，可以决定是否继续。' }}
        </text>
      </view>

      <view class="summary-card glass-card">
        <view class="summary-grid">
          <view class="summary-item">
            <text class="summary-label">目的地</text>
            <text class="summary-value">{{ state.destination || '待填写' }}</text>
          </view>
          <view class="summary-item">
            <text class="summary-label">开始日期</text>
            <text class="summary-value">{{ formatDate(state.travel_start_date) }}</text>
          </view>
          <view class="summary-item">
            <text class="summary-label">结束日期</text>
            <text class="summary-value">{{ formatDate(state.travel_end_date) }}</text>
          </view>
          <view class="summary-item">
            <text class="summary-label">决定截止</text>
            <text class="summary-value">{{ formatDateTime(currentCandidate && currentCandidate.decision_expires_at) }}</text>
          </view>
        </view>
      </view>

      <view v-if="currentCandidate" class="candidate-card glass-card">
        <view class="candidate-header">
          <view class="candidate-user" @tap="openUser(currentCandidate.peer_user_id)">
            <image class="candidate-avatar" :src="currentCandidate.peer_avatar" mode="aspectFill" />
            <view class="candidate-copy">
              <text class="candidate-name">{{ currentCandidate.peer_nickname || '候选搭子' }}</text>
              <text class="candidate-link">点击查看主页</text>
            </view>
          </view>
          <text class="candidate-status" :class="decisionClass">{{ decisionText }}</text>
        </view>

        <view class="summary-grid compact-grid">
          <view class="summary-item">
            <text class="summary-label">匹配理由</text>
            <text class="summary-value multiline">{{ currentCandidate.match_summary || '地点和日期已经重叠。' }}</text>
          </view>
          <view class="summary-item">
            <text class="summary-label">建议见面地</text>
            <text class="summary-value multiline">{{ currentCandidate.meeting_place_text || '待生成' }}</text>
          </view>
        </view>

        <view v-if="!hasAcceptedCandidate" class="action-row">
          <view class="secondary-action action-half" :class="{ disabled: busy }" @tap="handleRejectCandidate">不合适</view>
          <view class="primary-action action-half" :class="{ disabled: busy }" @tap="handleAcceptCandidate">我愿意</view>
        </view>
      </view>
    </view>

    <view v-else-if="currentView === 'accepted'" class="panel-stack">
      <view class="status-card glass-card">
        <text class="section-kicker">Confirmed</text>
        <text class="state-title">你们已经互相同意</text>
        <text class="state-desc">见面时间和地点已经生成，双方都可以各留一次备注。</text>
      </view>

      <view v-if="currentPair" class="candidate-card glass-card">
        <view class="candidate-header">
          <view class="candidate-user" @tap="openUser(currentPair.peer_user_id)">
            <image class="candidate-avatar" :src="currentPair.peer_avatar" mode="aspectFill" />
            <view class="candidate-copy">
              <text class="candidate-name">{{ currentPair.peer_nickname || '搭子' }}</text>
              <text class="candidate-link">点击查看主页</text>
            </view>
          </view>
          <text class="candidate-status accepted">已确认</text>
        </view>

        <view class="summary-grid compact-grid">
          <view class="summary-item">
            <text class="summary-label">目的地</text>
            <text class="summary-value">{{ state.destination || '待填写' }}</text>
          </view>
          <view class="summary-item">
            <text class="summary-label">日期范围</text>
            <text class="summary-value">{{ formatDate(state.travel_start_date) }} - {{ formatDate(state.travel_end_date) }}</text>
          </view>
          <view class="summary-item">
            <text class="summary-label">见面时间</text>
            <text class="summary-value">{{ formatDateTime(currentPair.meet_time) }}</text>
          </view>
          <view class="summary-item">
            <text class="summary-label">见面地点</text>
            <text class="summary-value multiline">{{ currentPair.meet_location_text || '待生成' }}</text>
          </view>
        </view>

        <view class="remark-block">
          <text class="summary-label">对方备注</text>
          <text class="remark-text">{{ currentPair.peer_remark || '对方暂时还没填写备注。' }}</text>
        </view>
      </view>

      <view v-if="currentPair && !currentPair.my_remark" class="field-card glass-card">
        <text class="field-label">我的备注（只能提交一次）</text>
        <textarea
          v-model="remarkText"
          class="field-textarea"
          maxlength="120"
          placeholder="例如：我会背黑色双肩包，预计提前 10 分钟到。"
          placeholder-style="color: rgba(246,240,232,0.24)"
        />
        <button class="primary-button submit-button" :class="{ disabled: busy }" @tap="submitRemark">提交备注</button>
      </view>

      <view v-else-if="currentPair" class="hint-card glass-card">
        <text>我的备注：{{ currentPair.my_remark }}</text>
      </view>
    </view>

    <view v-else class="panel-stack">
      <view class="status-card glass-card">
        <text class="section-kicker">Ended</text>
        <text class="state-title">{{ endTitle }}</text>
        <text class="state-desc">{{ endDescription }}</text>
      </view>

      <view v-if="state.request_id" class="summary-card glass-card">
        <view class="summary-grid">
          <view class="summary-item">
            <text class="summary-label">目的地</text>
            <text class="summary-value">{{ state.destination || '待填写' }}</text>
          </view>
          <view class="summary-item">
            <text class="summary-label">开始日期</text>
            <text class="summary-value">{{ formatDate(state.travel_start_date) }}</text>
          </view>
          <view class="summary-item">
            <text class="summary-label">结束日期</text>
            <text class="summary-value">{{ formatDate(state.travel_end_date) }}</text>
          </view>
          <view class="summary-item">
            <text class="summary-label">状态</text>
            <text class="summary-value">{{ endTitle }}</text>
          </view>
        </view>
      </view>

      <button class="primary-button submit-button" :class="{ disabled: busy }" @tap="beginEdit">重新填写条件</button>
    </view>

    <view v-if="showCandidatePopup && currentCandidate" class="popup-mask" @tap.self="dismissCandidatePopup">
      <view class="popup-card glass-card">
        <text class="popup-title">找到一位候选搭子</text>
        <text class="popup-desc">{{ currentCandidate.match_summary || '地点和日期已经重叠，可以先看看对方。' }}</text>

        <view class="candidate-card popup-inner-card">
          <view class="candidate-header">
            <view class="candidate-user" @tap="openUser(currentCandidate.peer_user_id)">
              <image class="candidate-avatar" :src="currentCandidate.peer_avatar" mode="aspectFill" />
              <view class="candidate-copy">
                <text class="candidate-name">{{ currentCandidate.peer_nickname || '候选搭子' }}</text>
                <text class="candidate-link">点击查看主页</text>
              </view>
            </view>
          </view>
          <view class="summary-grid compact-grid">
            <view class="summary-item">
              <text class="summary-label">建议见面地</text>
              <text class="summary-value multiline">{{ currentCandidate.meeting_place_text || '待生成' }}</text>
            </view>
            <view class="summary-item">
              <text class="summary-label">决定截止</text>
              <text class="summary-value">{{ formatDateTime(currentCandidate.decision_expires_at) }}</text>
            </view>
          </view>
        </view>

        <view class="action-row">
          <view class="secondary-action action-half" @tap="dismissCandidatePopup">稍后再看</view>
          <view class="primary-action action-half" :class="{ disabled: busy }" @tap="handleAcceptCandidate">我愿意</view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import AppHeader from '../../components/common/AppHeader.vue'
import {
  acceptRealtimeCandidate,
  cancelRealtimeMatch,
  createRealtimeMatch,
  getCurrentRealtimeMatch,
  rejectRealtimeCandidate,
  sendRealtimeRemark
} from '../../api/modules/match'
import { go } from '../../utils/navigation'

const DISMISSED_CANDIDATE_KEY = 'faraway_match_dismissed_candidate'
const POLL_INTERVAL = 5000
const PREFERENCE_TAGS = ['特种兵', '慢旅行', '拍照', '美食', '自然风光', '人文历史', '早起', '夜景']

function createEmptyForm() {
  return {
    destination: '',
    travel_start_date: '',
    travel_end_date: '',
    preference_tags: [],
    preference_text: ''
  }
}

export default {
  components: {
    AppHeader
  },
  data() {
    return {
      preferenceTagOptions: PREFERENCE_TAGS,
      form: createEmptyForm(),
      state: {
        active: false
      },
      editing: false,
      busy: false,
      showCandidatePopup: false,
      remarkText: '',
      pollTimer: null,
      lastCandidateNoticeId: '',
      lastPairNoticeId: ''
    }
  },
  computed: {
    currentView() {
      const status = this.state && this.state.status
      if (status === 'matched_accepted') {
        return 'accepted'
      }
      if (status === 'matched_waiting_decision') {
        return 'waiting'
      }
      if (this.editing) {
        return 'form'
      }
      if (status === 'pending') {
        return 'pending'
      }
      if (status === 'failed' || status === 'cancelled' || status === 'finished') {
        return 'end'
      }
      return 'form'
    },
    currentCandidate() {
      const candidate = this.state && this.state.candidate
      return candidate && typeof candidate === 'object' ? candidate : null
    },
    currentPair() {
      const pair = this.state && this.state.pair
      return pair && typeof pair === 'object' ? pair : null
    },
    stateTags() {
      return Array.isArray(this.state && this.state.preference_tags) ? this.state.preference_tags : []
    },
    canReturnToPending() {
      return this.editing && this.state && this.state.status === 'pending'
    },
    hasAcceptedCandidate() {
      return !!(this.currentCandidate && this.currentCandidate.my_decision === 'accepted')
    },
    decisionText() {
      if (!this.currentCandidate) {
        return '待决定'
      }
      if (this.currentCandidate.my_decision === 'accepted') {
        return '等待对方'
      }
      if (this.currentCandidate.peer_decision === 'accepted') {
        return '对方已同意'
      }
      return '待决定'
    },
    decisionClass() {
      return this.hasAcceptedCandidate ? 'accepted' : 'pending'
    },
    submitButtonText() {
      return this.state && this.state.status === 'pending' ? '更新匹配条件' : '开始匹配'
    },
    endTitle() {
      const status = this.state && this.state.status
      if (status === 'failed') {
        return '本轮没有匹配成功'
      }
      if (status === 'cancelled') {
        return '本轮匹配已取消'
      }
      if (status === 'finished') {
        return '本次见面流程已结束'
      }
      return '当前没有进行中的匹配'
    },
    endDescription() {
      const status = this.state && this.state.status
      if (status === 'failed') {
        return '在截止时间前没有找到更合适的对象，可以直接调整条件重新发起。'
      }
      if (status === 'cancelled') {
        return '你已经取消当前匹配，重新填写后可以再次发起。'
      }
      if (status === 'finished') {
        return '这次搭子流程已经自然结束，如果还想继续找人，可以再开一轮。'
      }
      return '先填写目的地、日期和偏好，系统才会开始匹配。'
    }
  },
  onShow() {
    this.loadCurrentState()
  },
  onHide() {
    this.stopPolling()
  },
  onUnload() {
    this.stopPolling()
  },
  methods: {
    hasTag(tag) {
      return this.form.preference_tags.includes(tag)
    },
    toggleTag(tag) {
      const current = Array.isArray(this.form.preference_tags) ? [...this.form.preference_tags] : []
      const index = current.indexOf(tag)
      if (index >= 0) {
        current.splice(index, 1)
      } else {
        current.push(tag)
      }
      this.form.preference_tags = current
    },
    beginEdit() {
      this.fillFormFromState()
      this.editing = true
    },
    cancelEdit() {
      this.editing = false
    },
    fillFormFromState() {
      this.form = {
        destination: this.state.destination || '',
        travel_start_date: this.state.travel_start_date || '',
        travel_end_date: this.state.travel_end_date || '',
        preference_tags: Array.isArray(this.state.preference_tags) ? [...this.state.preference_tags] : [],
        preference_text: this.state.preference_text || ''
      }
    },
    validateForm() {
      const destination = (this.form.destination || '').trim()
      const startDate = (this.form.travel_start_date || '').trim()
      const endDate = (this.form.travel_end_date || '').trim()
      const hasPreference = (Array.isArray(this.form.preference_tags) && this.form.preference_tags.length > 0)
        || (this.form.preference_text || '').trim()

      if (!destination) {
        return '请先填写目的地'
      }
      if (!startDate || !endDate) {
        return '请先填写完整日期'
      }
      if (!/^\d{4}-\d{2}-\d{2}$/.test(startDate) || !/^\d{4}-\d{2}-\d{2}$/.test(endDate)) {
        return '日期格式需为 YYYY-MM-DD'
      }
      if (endDate < startDate) {
        return '结束日期不能早于开始日期'
      }
      if (!hasPreference) {
        return '至少选择一个偏好标签或填写补充说明'
      }
      return ''
    },
    async loadCurrentState(silentError = false) {
      try {
        const previousState = this.state && typeof this.state === 'object' ? { ...this.state } : { active: false }
        const result = await getCurrentRealtimeMatch()
        this.state = result && typeof result === 'object' ? result : { active: false }
        if (this.currentPair && this.currentPair.my_remark) {
          this.remarkText = ''
        }
        this.maybeShowCandidatePopup()
        this.maybeNotifyRealtimeState(previousState)
        this.syncPolling()
      } catch (error) {
        this.stopPolling()
        if (!silentError) {
          this.showError(error, '获取当前匹配状态失败')
        }
      }
    },
    syncPolling() {
      const status = this.state && this.state.status
      if (status === 'pending' || status === 'matched_waiting_decision') {
        if (this.pollTimer) {
          return
        }
        this.pollTimer = setInterval(() => {
          this.loadCurrentState(true)
        }, POLL_INTERVAL)
        return
      }
      this.stopPolling()
    },
    stopPolling() {
      if (!this.pollTimer) {
        return
      }
      clearInterval(this.pollTimer)
      this.pollTimer = null
    },
    maybeShowCandidatePopup() {
      if (!this.currentCandidate || this.state.status !== 'matched_waiting_decision') {
        this.showCandidatePopup = false
        return
      }
      if (this.currentCandidate.my_decision === 'accepted') {
        this.showCandidatePopup = false
        return
      }
      const dismissedId = uni.getStorageSync(DISMISSED_CANDIDATE_KEY) || ''
      this.showCandidatePopup = dismissedId !== this.currentCandidate.candidate_id
    },
    maybeNotifyRealtimeState(previousState) {
      const previousStatus = previousState && previousState.status ? previousState.status : ''
      const currentStatus = this.state && this.state.status ? this.state.status : ''
      if (currentStatus === 'matched_waiting_decision' && this.currentCandidate && this.currentCandidate.candidate_id !== this.lastCandidateNoticeId) {
        this.lastCandidateNoticeId = this.currentCandidate.candidate_id
        if (previousStatus !== 'matched_waiting_decision' || !previousState.candidate || previousState.candidate.candidate_id !== this.currentCandidate.candidate_id) {
          uni.showToast({
            title: '已为你找到新的搭子候选',
            icon: 'none'
          })
        }
      }
      if (currentStatus === 'matched_accepted' && this.currentPair && this.currentPair.pair_id !== this.lastPairNoticeId) {
        this.lastPairNoticeId = this.currentPair.pair_id
        uni.showModal({
          title: '匹配成功',
          content: '双方已确认成功，快去查看对方信息并联系吧。',
          showCancel: false,
          confirmText: '我知道了'
        })
      }
    },
    rememberDismissedCandidate() {
      if (!this.currentCandidate) {
        return
      }
      uni.setStorageSync(DISMISSED_CANDIDATE_KEY, this.currentCandidate.candidate_id)
    },
    dismissCandidatePopup() {
      this.rememberDismissedCandidate()
      this.showCandidatePopup = false
    },
    async submitRealtimeMatch() {
      const message = this.validateForm()
      if (message) {
        uni.showToast({
          title: message,
          icon: 'none'
        })
        return
      }
      if (this.busy) {
        return
      }
      this.busy = true
      try {
        await createRealtimeMatch({
          destination: this.form.destination.trim(),
          travel_start_date: this.form.travel_start_date.trim(),
          travel_end_date: this.form.travel_end_date.trim(),
          preference_tags: Array.isArray(this.form.preference_tags) ? this.form.preference_tags : [],
          preference_text: (this.form.preference_text || '').trim()
        })
        this.editing = false
        this.showCandidatePopup = false
        await this.loadCurrentState()
        uni.showToast({
          title: '已开始匹配',
          icon: 'none'
        })
      } catch (error) {
        this.showError(error, '提交匹配失败')
      } finally {
        this.busy = false
      }
    },
    async cancelPendingMatch() {
      if (this.busy || !this.state.request_id || this.state.status !== 'pending') {
        return
      }
      this.busy = true
      try {
        await cancelRealtimeMatch(this.state.request_id)
        this.editing = false
        await this.loadCurrentState()
        uni.showToast({
          title: '已取消',
          icon: 'none'
        })
      } catch (error) {
        this.showError(error, '取消匹配失败')
      } finally {
        this.busy = false
      }
    },
    async handleAcceptCandidate() {
      if (this.busy || !this.currentCandidate || this.hasAcceptedCandidate) {
        return
      }
      this.busy = true
      try {
        this.rememberDismissedCandidate()
        this.showCandidatePopup = false
        await acceptRealtimeCandidate(this.currentCandidate.candidate_id)
        await this.loadCurrentState()
      } catch (error) {
        this.showError(error, '操作失败')
      } finally {
        this.busy = false
      }
    },
    async handleRejectCandidate() {
      if (this.busy || !this.currentCandidate) {
        return
      }
      this.busy = true
      try {
        this.rememberDismissedCandidate()
        this.showCandidatePopup = false
        await rejectRealtimeCandidate(this.currentCandidate.candidate_id)
        await this.loadCurrentState()
        uni.showToast({
          title: '已回到匹配中',
          icon: 'none'
        })
      } catch (error) {
        this.showError(error, '操作失败')
      } finally {
        this.busy = false
      }
    },
    async submitRemark() {
      if (this.busy || !this.currentPair || this.currentPair.my_remark) {
        return
      }
      const remark = (this.remarkText || '').trim()
      if (!remark) {
        uni.showToast({
          title: '请先填写备注',
          icon: 'none'
        })
        return
      }
      this.busy = true
      try {
        await sendRealtimeRemark(this.currentPair.pair_id, remark)
        this.remarkText = ''
        await this.loadCurrentState()
        uni.showToast({
          title: '备注已提交',
          icon: 'none'
        })
      } catch (error) {
        this.showError(error, '备注提交失败')
      } finally {
        this.busy = false
      }
    },
    showError(error, fallbackTitle) {
      uni.showToast({
        title: (error && error.message) || fallbackTitle,
        icon: 'none'
      })
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
    openUser(userId) {
      if (!userId) {
        return
      }
      go(`/pages/user-profile/index?userId=${userId}`)
    },
    openRecords() {
      go('/pages/my-partners/index')
    }
  }
}
</script>

<style scoped lang="scss">
.record-entry {
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

.hero-card,
.field-card,
.status-card,
.summary-card,
.hint-card,
.candidate-card,
.popup-card {
  border-radius: 30rpx;
  padding: 28rpx;
}

.hero-title,
.state-title {
  display: block;
  margin-top: 12rpx;
  font-size: 40rpx;
  line-height: 1.2;
  font-weight: 700;
  color: #f6f0e8;
}

.hero-desc,
.state-desc,
.hint-card text,
.candidate-link,
.popup-desc,
.note-text,
.remark-text {
  display: block;
  margin-top: 14rpx;
  font-size: 24rpx;
  line-height: 1.7;
  color: rgba(246, 240, 232, 0.68);
}

.panel-stack {
  display: flex;
  flex-direction: column;
  gap: 22rpx;
  margin-top: 26rpx;
}

.two-field-row,
.action-row,
.candidate-header,
.candidate-user,
.summary-grid {
  display: flex;
}

.two-field-row,
.action-row {
  gap: 20rpx;
}

.field-half,
.action-half {
  flex: 1;
}

.field-label,
.summary-label {
  display: block;
  font-size: 22rpx;
  letter-spacing: 4rpx;
  color: rgba(246, 240, 232, 0.46);
}

.field-input,
.field-textarea,
.summary-value,
.candidate-name {
  color: #f6f0e8;
}

.field-input {
  margin-top: 16rpx;
  font-size: 34rpx;
}

.field-textarea {
  width: 100%;
  min-height: 180rpx;
  margin-top: 16rpx;
  font-size: 28rpx;
  line-height: 1.7;
}

.tag-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
  margin-top: 18rpx;
}

.tag-option {
  min-width: 132rpx;
  height: 72rpx;
  padding: 0 24rpx;
  border-radius: 999rpx;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  color: rgba(246, 240, 232, 0.72);
  background: rgba(255, 255, 255, 0.06);
  border: 1rpx solid rgba(255, 255, 255, 0.08);
}

.tag-option.active {
  background: rgba(236, 214, 179, 0.18);
  border-color: rgba(236, 214, 179, 0.36);
  color: #ecd6b3;
}

.submit-button {
  width: 100%;
}

.summary-grid {
  flex-wrap: wrap;
  gap: 18rpx;
}

.summary-item {
  width: calc(50% - 9rpx);
  min-height: 116rpx;
  padding: 20rpx;
  border-radius: 24rpx;
  background: rgba(255, 255, 255, 0.04);
  box-sizing: border-box;
}

.compact-grid .summary-item {
  width: 100%;
  min-height: auto;
}

.summary-value {
  display: block;
  margin-top: 12rpx;
  font-size: 28rpx;
  line-height: 1.5;
  font-weight: 700;
}

.summary-value.multiline {
  white-space: normal;
}

.chips-row {
  display: flex;
  flex-wrap: wrap;
  gap: 14rpx;
  margin-top: 22rpx;
}

.tag-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10rpx 20rpx;
  border-radius: 999rpx;
  background: rgba(236, 214, 179, 0.12);
  color: #ecd6b3;
  font-size: 22rpx;
}

.secondary-action,
.danger-action,
.primary-action {
  min-height: 88rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26rpx;
  font-weight: 700;
}

.secondary-action {
  background: rgba(255, 255, 255, 0.08);
  color: #f6f0e8;
  border: 1rpx solid rgba(255, 255, 255, 0.08);
}

.danger-action {
  background: rgba(255, 141, 122, 0.16);
  color: #ffb0a1;
  border: 1rpx solid rgba(255, 141, 122, 0.14);
}

.primary-action {
  background: #ecd6b3;
  color: #0c1320;
}

.candidate-header {
  align-items: center;
  justify-content: space-between;
  gap: 18rpx;
}

.candidate-user {
  flex: 1;
  align-items: center;
}

.candidate-avatar {
  width: 92rpx;
  height: 92rpx;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
}

.candidate-copy {
  margin-left: 18rpx;
}

.candidate-name {
  display: block;
  font-size: 30rpx;
  font-weight: 700;
}

.candidate-link {
  margin-top: 8rpx;
  font-size: 22rpx;
}

.candidate-status {
  min-width: 132rpx;
  height: 56rpx;
  padding: 0 18rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22rpx;
  font-weight: 700;
}

.candidate-status.pending {
  background: rgba(236, 214, 179, 0.12);
  color: #ecd6b3;
}

.candidate-status.accepted {
  background: rgba(108, 214, 167, 0.14);
  color: #6cd6a7;
}

.remark-block {
  margin-top: 24rpx;
  padding-top: 24rpx;
  border-top: 1rpx solid rgba(255, 255, 255, 0.06);
}

.popup-mask {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32rpx;
  background: rgba(4, 10, 18, 0.7);
  z-index: 20;
  box-sizing: border-box;
}

.popup-card {
  width: 100%;
  max-width: 640rpx;
}

.popup-title {
  display: block;
  font-size: 36rpx;
  font-weight: 700;
  color: #f6f0e8;
}

.popup-inner-card {
  padding: 0;
  margin-top: 24rpx;
  background: transparent;
  border: none;
  box-shadow: none;
}

.disabled {
  opacity: 0.56;
  pointer-events: none;
}
</style>
