<template>
  <view class="page-shell">
    <AppHeader title="我的点赞" subtitle="Likes" fallback="/pages/profile/index" />
    <view class="two-column-grid">
      <view v-for="item in items" :key="`${item.contentType}-${item.id}`" class="content-card simple-card" @tap="openItem(item)">
        <image class="simple-image" :src="item.coverUrl" mode="aspectFill" />
        <view class="simple-body">
          <text class="simple-type">{{ item.contentType === 'vlog' ? 'Vlog' : '攻略' }}</text>
          <text class="simple-title">{{ item.title }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import AppHeader from '../../components/common/AppHeader.vue'
import { getMyLikeContents } from '../../api/modules/user'
import { go } from '../../utils/navigation'

export default {
  components: {
    AppHeader
  },
  data() {
    return {
      items: []
    }
  },
  onShow() {
    this.loadData()
  },
  methods: {
    async loadData() {
      const result = await getMyLikeContents()
      this.items = result.list
    },
    openItem(item) {
      if (item.contentType === 'vlog' || item.type === 'vlog') {
        go(`/pages/vlog-detail/index?id=${item.id}`)
        return
      }
      go(`/pages/strategy-detail/index?id=${item.id}`)
    }
  }
}
</script>

<style scoped lang="scss">
.simple-card {
  overflow: hidden;
}

.simple-image {
  width: 100%;
  height: 260rpx;
}

.simple-body {
  padding: 18rpx;
}

.simple-type,
.simple-title {
  display: block;
}

.simple-type {
  font-size: 20rpx;
  color: rgba(246, 240, 232, 0.46);
}

.simple-title {
  margin-top: 8rpx;
  font-size: 24rpx;
  line-height: 1.5;
}
</style>
