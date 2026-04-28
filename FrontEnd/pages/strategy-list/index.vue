<template>
  <view class="page-shell with-safe-bottom">
    <view class="top-block">
      <text class="section-kicker">Strategy</text>
      <text class="section-title">把目的地拆成你能立刻出发的路线</text>
    </view>

    <view class="search-bar glass-card" @tap="openSearch">
      <text class="search-text">{{ keyword || '搜索目的地、主题或攻略...' }}</text>
    </view>

    <scroll-view scroll-x class="category-scroll" show-scrollbar="false">
      <view class="category-row">
        <view
          v-for="item in categories"
          :key="item"
          class="category-pill"
          :class="{ active: item === activeCategory }"
          @tap="switchCategory(item)"
        >
          {{ item }}
        </view>
      </view>
    </scroll-view>

    <view class="list-column">
      <view v-for="item in list" :key="item.id" class="strategy-card content-card" @tap="openDetail(item.id)">
        <image class="strategy-image" :src="item.coverUrl" mode="aspectFill" />
        <view class="strategy-body">
          <text class="strategy-location">{{ item.destination }}</text>
          <text class="strategy-title">{{ item.title }}</text>
          <text class="strategy-summary">{{ item.summary }}</text>
          <view class="tag-row">
            <text v-for="tag in item.tags.slice(0, 2)" :key="tag" class="tag-chip">{{ tag }}</text>
          </view>
        </view>
      </view>
    </view>
    <FloatingPublishButton />
  </view>
</template>

<script>
import { STRATEGY_CATEGORIES } from '../../constants/enums'
import { getStrategyList } from '../../api/modules/strategy'
import { go } from '../../utils/navigation'
import FloatingPublishButton from '../../components/common/FloatingPublishButton.vue'

export default {
  components: {
    FloatingPublishButton
  },
  data() {
    return {
      categories: STRATEGY_CATEGORIES,
      activeCategory: '全部',
      keyword: '',
      list: []
    }
  },
  onLoad(options) {
    this.keyword = (options && options.keyword) || ''
    this.fetchList()
  },
  methods: {
    async fetchList() {
      const result = await getStrategyList({
        category: this.activeCategory,
        keyword: this.keyword
      })
      this.list = result.list
    },
    switchCategory(item) {
      this.activeCategory = item
      this.fetchList()
    },
    openSearch() {
      go(`/pages/search-result/index?keyword=${this.keyword}&type=strategy`)
    },
    openDetail(id) {
      go(`/pages/strategy-detail/index?id=${id}`)
    }
  }
}
</script>

<style scoped lang="scss">
.search-bar {
  margin-top: 32rpx;
  padding: 28rpx 30rpx;
  border-radius: 28rpx;
}

.search-text {
  font-size: 28rpx;
  color: rgba(246, 240, 232, 0.72);
}

.category-scroll {
  margin-top: 28rpx;
  white-space: nowrap;
}

.category-row {
  display: inline-flex;
  gap: 16rpx;
}

.category-pill {
  padding: 18rpx 28rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.06);
  color: rgba(246, 240, 232, 0.7);
  font-size: 24rpx;
}

.category-pill.active {
  background: #ecd6b3;
  color: #07111f;
  font-weight: 700;
}

.list-column {
  margin-top: 28rpx;
  display: flex;
  flex-direction: column;
  gap: 22rpx;
}

.strategy-card {
  overflow: hidden;
}

.strategy-image {
  width: 100%;
  height: 360rpx;
}

.strategy-body {
  padding: 24rpx;
}

.strategy-location {
  display: block;
  font-size: 22rpx;
  letter-spacing: 4rpx;
  color: rgba(246, 240, 232, 0.5);
}

.strategy-title {
  display: block;
  margin-top: 10rpx;
  font-size: 34rpx;
  line-height: 1.35;
  color: #f6f0e8;
  font-weight: 700;
}

.strategy-summary {
  display: block;
  margin-top: 12rpx;
  font-size: 24rpx;
  line-height: 1.7;
  color: rgba(246, 240, 232, 0.66);
}

.tag-row {
  display: flex;
  gap: 12rpx;
  margin-top: 20rpx;
}
</style>
