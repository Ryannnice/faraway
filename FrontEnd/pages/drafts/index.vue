<template>
  <view class="page-shell">
    <AppHeader title="草稿箱" subtitle="Drafts" fallback="/pages/profile/index" />
    <view class="list-column">
      <view v-for="item in list" :key="item.id" class="draft-card glass-card" @tap="openDraft(item)">
        <text class="draft-type">{{ item.draftType === 'strategy' ? '攻略草稿' : '发布草稿' }}</text>
        <text class="draft-title">{{ item.title }}</text>
        <text class="draft-time">{{ item.updatedAt }}</text>
      </view>
    </view>
  </view>
</template>

<script>
import AppHeader from '../../components/common/AppHeader.vue'
import { getMyDrafts } from '../../api/modules/user'
import { setPendingDraft } from '../../utils/storage'
import { go } from '../../utils/navigation'

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
      const result = await getMyDrafts()
      this.list = result.list || []
    },
    openDraft(item) {
      setPendingDraft(item)
      if (item.draftType === 'strategy') {
        go('/pages/strategy-form/index?draft=1')
        return
      }
      go('/pages/upload/index?draft=1')
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

.draft-card {
  padding: 26rpx;
  border-radius: 28rpx;
}

.draft-type,
.draft-time {
  display: block;
  font-size: 22rpx;
  color: rgba(246, 240, 232, 0.48);
}

.draft-title {
  display: block;
  margin-top: 10rpx;
  font-size: 28rpx;
  line-height: 1.6;
}

.draft-time {
  margin-top: 14rpx;
}
</style>
