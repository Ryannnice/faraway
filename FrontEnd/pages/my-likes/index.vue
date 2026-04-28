<template>
  <view class="page-shell">
    <AppHeader title="我的点赞" subtitle="Likes" fallback="/pages/profile/index" />
    <view class="two-column-grid">
      <view v-for="item in items" :key="`${item.contentType}-${item.id}`" class="content-card simple-card" @tap="openItem(item)">
        <video
          v-if="(item.contentType === 'vlog' || item.type === 'vlog') && hasVideo(item)"
          class="simple-image"
          :src="getVideoUrl(item)"
          :poster="getPosterUrl(item)"
          object-fit="cover"
          autoplay
          muted
          loop
          :controls="false"
          :show-center-play-btn="false"
          :enable-progress-gesture="false"
        />
        <image v-else class="simple-image" :src="item.coverUrl" mode="aspectFill" />
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
import { getPostPosterUrl, getPostVideoUrl, hasPostVideo } from '../../utils/post-media'
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
    hasVideo(item) {
      return hasPostVideo(item)
    },
    getVideoUrl(item) {
      return getPostVideoUrl(item)
    },
    getPosterUrl(item) {
      return getPostPosterUrl(item)
    },
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
