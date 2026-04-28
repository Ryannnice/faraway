<template>
  <view class="page-shell">
    <AppHeader title="搜索结果" subtitle="Search" :fallback="fallback" />
    <view class="search-bar glass-card">
      <input v-model="keyword" class="search-input" placeholder="搜索目的地、主题或 Vlog..." placeholder-style="color: rgba(246,240,232,0.24)" @confirm="fetchData" />
    </view>

    <view class="tab-row">
      <view v-for="item in tabs" :key="item" class="tab-pill" :class="{ active: item === type }" @tap="switchType(item)">
        {{ labelMap[item] }}
      </view>
    </view>

    <view class="two-column-grid">
      <view v-for="item in mixedList" :key="`${item.contentType}-${item.id}`" class="content-card search-card" @tap="openItem(item)">
        <image class="search-image" :src="item.coverUrl" mode="aspectFill" />
        <view class="search-body">
          <text class="search-type">{{ item.contentType === 'strategy' ? '攻略' : 'Vlog' }}</text>
          <text class="search-title">{{ item.title }}</text>
          <text class="search-sub">{{ item.contentType === 'strategy' ? item.destination : item.location }}</text>
        </view>
      </view>
    </view>
    <EmptyState v-if="!mixedList.length" title="未找到相关内容" description="换个关键词试试看，或者先逛逛首页灵感。" />
  </view>
</template>

<script>
import AppHeader from '../../components/common/AppHeader.vue'
import EmptyState from '../../components/common/EmptyState.vue'
import { SEARCH_TYPES } from '../../constants/enums'
import { searchAll } from '../../api/modules/search'
import { saveSearchKeyword } from '../../utils/storage'
import { go } from '../../utils/navigation'

export default {
  components: {
    AppHeader,
    EmptyState
  },
  data() {
    return {
      tabs: SEARCH_TYPES,
      labelMap: {
        all: '全部',
        strategy: '攻略',
        vlog: 'Vlog'
      },
      keyword: '',
      type: 'all',
      fallback: '/pages/home/index',
      result: {
        strategyList: [],
        vlogList: []
      }
    }
  },
  computed: {
    mixedList() {
      if (this.type === 'strategy') {
        return this.result.strategyList.map((item) => Object.assign({}, item, { contentType: 'strategy' }))
      }
      if (this.type === 'vlog') {
        return this.result.vlogList.map((item) => Object.assign({}, item, { contentType: 'vlog' }))
      }
      return this.result.strategyList
        .map((item) => Object.assign({}, item, { contentType: 'strategy' }))
        .concat(this.result.vlogList.map((item) => Object.assign({}, item, { contentType: 'vlog' })))
    }
  },
  onLoad(options) {
    this.keyword = (options && options.keyword) || ''
    this.type = (options && options.type) || 'all'
    this.fetchData()
  },
  methods: {
    async fetchData() {
      saveSearchKeyword(this.keyword)
      this.result = await searchAll({
        keyword: this.keyword,
        type: this.type
      })
    },
    switchType(nextType) {
      this.type = nextType
      this.fetchData()
    },
    openItem(item) {
      if (item.contentType === 'vlog') {
        go(`/pages/vlog-detail/index?id=${item.id}`)
        return
      }
      go(`/pages/strategy-detail/index?id=${item.id}`)
    }
  }
}
</script>

<style scoped lang="scss">
.search-bar {
  padding: 24rpx 28rpx;
  border-radius: 28rpx;
}

.search-input {
  color: #f6f0e8;
  font-size: 28rpx;
}

.tab-row {
  display: flex;
  gap: 14rpx;
  margin: 24rpx 0;
}

.tab-pill {
  padding: 16rpx 26rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.06);
  color: rgba(246, 240, 232, 0.7);
  font-size: 24rpx;
}

.tab-pill.active {
  background: #ecd6b3;
  color: #07111f;
  font-weight: 700;
}

.search-card {
  overflow: hidden;
}

.search-image {
  width: 100%;
  height: 280rpx;
}

.search-body {
  padding: 18rpx;
}

.search-type,
.search-sub {
  display: block;
  font-size: 22rpx;
  color: rgba(246, 240, 232, 0.48);
}

.search-title {
  display: block;
  margin-top: 8rpx;
  min-height: 72rpx;
  font-size: 24rpx;
  line-height: 1.5;
}

.search-sub {
  margin-top: 10rpx;
}
</style>
