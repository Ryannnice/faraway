<template>
  <view class="page-shell">
    <AppHeader title="我的发布" subtitle="My Posts" fallback="/pages/profile/index" />
    <view class="list-column">
      <view v-for="item in items" :key="item.id" class="content-card row-card" @tap="openItem(item)">
        <video
          v-if="hasVideo(item)"
          class="row-image"
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
        <image v-else class="row-image" :src="item.coverUrl" mode="aspectFill" />
        <view class="row-body">
          <text class="row-type">{{ item.type === 'vlog' ? 'Vlog' : '攻略' }}</text>
          <text class="row-title">{{ item.title }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import AppHeader from '../../components/common/AppHeader.vue'
import { getUserPublishedContent } from '../../api/modules/user'
import { useUserStore } from '../../stores/user'
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
      const userStore = useUserStore()
      const userId = userStore.userInfo && userStore.userInfo.id
      if (!userId) {
        this.items = []
        return
      }
      const result = await getUserPublishedContent(userId)
      this.items = result.list || []
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
.list-column {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.row-card {
  display: flex;
  overflow: hidden;
}

.row-image {
  width: 220rpx;
  height: 220rpx;
}

.row-body {
  flex: 1;
  padding: 22rpx;
}

.row-type {
  display: block;
  font-size: 22rpx;
  color: rgba(246, 240, 232, 0.48);
}

.row-title {
  display: block;
  margin-top: 14rpx;
  font-size: 30rpx;
  line-height: 1.5;
}
</style>
