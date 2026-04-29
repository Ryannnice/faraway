<template>
  <view class="page-shell">
    <AppHeader title="AI 做攻略" subtitle="Exclusive Itinerary" fallback="/pages/home/index" />
    <view v-if="!result" class="form-stack">
      <view class="field glass-card" v-for="item in fields" :key="item.key">
        <text class="field-label">{{ item.label }}</text>
        <input v-model="form[item.key]" class="field-input" :placeholder="item.placeholder" placeholder-style="color: rgba(246,240,232,0.24)" />
      </view>
      <button class="primary-button" @tap="handleGenerate">开始定制</button>
    </view>
    <view v-else class="result-stack">
      <image class="result-image" src="https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&q=80&w=2000" mode="aspectFill" />
      <text class="section-kicker">Destination</text>
      <text class="section-title">{{ result.destination }}</text>
      <view class="content-block glass-card">
        <text class="content-text">{{ result.overview }}</text>
      </view>
      <view v-for="day in result.dailyPlans" :key="day.day" class="day-card glass-card">
        <text class="day-title">Day {{ day.day }}</text>
        <text class="content-text">{{ day.activities.join(' / ') }}</text>
      </view>
      <view class="action-row">
        <view class="pill-button secondary-btn" @tap="resetForm">重新填写</view>
        <view class="pill-button secondary-btn" @tap="saveDraft">保存草稿</view>
      </view>
      <view class="action-row publish-row">
        <view class="primary-button full-btn" @tap="publishStrategy">正式保存为攻略</view>
      </view>
    </view>
  </view>
</template>

<script>
import AppHeader from '../../components/common/AppHeader.vue'
import { createStrategy, saveStrategyDraft } from '../../api/modules/strategy'
import { generateStrategy } from '../../services/ai'
import { clearPendingDraft, getPendingDraft } from '../../utils/storage'
import { go } from '../../utils/navigation'

export default {
  components: {
    AppHeader
  },
  data() {
    return {
      form: {
        destination: '',
        days: '3',
        budget: '',
        hotelRequirement: '',
        allergies: '',
        pace: '',
        groupType: ''
      },
      fields: [
        { key: 'destination', label: '目标地点', placeholder: '例：冰岛、西藏、东京...' },
        { key: 'days', label: '旅行天数', placeholder: '想玩几天' },
        { key: 'budget', label: '预算范围', placeholder: '经济、舒适或奢华？' },
        { key: 'pace', label: '行程松紧', placeholder: '慢一点还是充实一点？' }
      ],
      result: null,
      generating: false
    }
  },
  onLoad(options) {
    if (options && options.draft) {
      this.restoreDraft()
    }
  },
  methods: {
    restoreDraft() {
      const draft = getPendingDraft()
      if (!draft || draft.draftType !== 'strategy' || !draft.payload) {
        return
      }
      this.form.destination = draft.payload.destination || ''
      this.form.days = String(draft.payload.days || 3)
      clearPendingDraft()
    },
    async handleGenerate() {
      if (!this.form.destination) {
        uni.showToast({
          title: '请先填写目标地点',
          icon: 'none'
        })
        return
      }

      this.generating = true
      uni.showLoading({
        title: 'AI 生成中...',
        mask: true
      })

      try {
        this.result = await generateStrategy(this.form)
      } catch (error) {
        uni.showToast({
          title: error && error.message ? error.message : '生成失败，请稍后重试',
          icon: 'none'
        })
      } finally {
        this.generating = false
        uni.hideLoading()
      }
    },
    resetForm() {
      this.result = null
    },
    buildStrategyPayload() {
      const destination = this.result && this.result.destination ? this.result.destination : this.form.destination
      const days = Number(this.form.days || 3)
      const title = `${destination} ${days}天 AI 行程攻略`
      const summary = this.result && this.result.overview ? this.result.overview.slice(0, 48) : `${destination} 行程规划`
      const content = this.result
        ? this.result.dailyPlans.map((day) => `Day ${day.day}: ${day.activities.join(' / ')}`).join('\n')
        : ''
      return {
        title,
        summary,
        content,
        destination,
        days,
        category: '自然风光',
        coverUrl: 'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&q=80&w=2000',
        tags: [destination, 'AI生成', this.form.pace].filter(Boolean)
      }
    },
    async saveDraft() {
      await saveStrategyDraft({
        ...this.buildStrategyPayload(),
        overview: this.result ? this.result.overview : '',
        dailyPlans: this.result ? this.result.dailyPlans : []
      })
      uni.showToast({
        title: '已保存到草稿箱',
        icon: 'none'
      })
      setTimeout(() => {
        go('/pages/drafts/index')
      }, 240)
    },
    async publishStrategy() {
      const saved = await createStrategy(this.buildStrategyPayload())
      uni.showToast({
        title: '已保存为攻略',
        icon: 'none'
      })
      setTimeout(() => {
        uni.redirectTo({
          url: `/pages/strategy-detail/index?id=${saved.id}&fromPublish=1`
        })
      }, 240)
    }
  }
}
</script>

<style scoped lang="scss">
.form-stack {
  display: flex;
  flex-direction: column;
  gap: 22rpx;
}

.field {
  padding: 26rpx 28rpx;
  border-radius: 28rpx;
}

.field-label {
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

.result-image {
  width: 100%;
  height: 420rpx;
  border-radius: 34rpx;
}

.content-block,
.day-card {
  margin-top: 24rpx;
  border-radius: 30rpx;
  padding: 26rpx;
}

.content-text {
  font-size: 28rpx;
  line-height: 1.8;
  color: rgba(246, 240, 232, 0.72);
}

.day-title {
  display: block;
  margin-bottom: 14rpx;
  font-size: 28rpx;
  font-weight: 700;
}

.action-row {
  display: flex;
  gap: 18rpx;
  margin-top: 28rpx;
}

.secondary-btn,
.half-btn {
  flex: 1;
}

.publish-row {
  margin-top: 16rpx;
}

.full-btn {
  width: 100%;
}
</style>
