<template>
  <view class="home-page">
    <image class="hero-bg" :src="heroImage" mode="aspectFill" />
    <view class="hero-mask" />
    <view class="hero-content">
      <view class="heading">
        <text class="section-kicker">Faraway Polaris</text>
        <text class="hero-title">来一次说走就走的旅行</text>
      </view>

      <view class="cta-row">
        <view class="pill-button cta" @tap="goStrategyForm">做攻略</view>
        <view class="pill-button cta" @tap="goMatch">找搭子</view>
      </view>

      <view class="search-box glass-card" @tap="goSearch('')">
        <text class="search-icon">⌕</text>
        <text class="search-placeholder">寻找你的远方...</text>
        <text class="search-divider">|</text>
        <text class="search-icon">◎</text>
      </view>
    </view>

    <view class="preview-panel glass-card">
      <view class="preview-head">
        <text class="section-kicker">Preview</text>
        <text class="preview-link" @tap="goStrategyList">进入攻略</text>
      </view>
      <scroll-view scroll-x class="preview-scroll" show-scrollbar="false">
        <view class="preview-row">
          <view v-for="item in previewItems" :key="item.id" class="preview-card" @tap="openPreview(item)">
            <video
              v-if="item.contentType === 'vlog' && hasVideo(item)"
              class="preview-image"
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
            <image v-else class="preview-image" :src="item.coverUrl" mode="aspectFill" />
            <view class="preview-mask" />
            <view class="preview-text">
              <text class="preview-type">{{ item.contentType === 'strategy' ? '攻略' : 'Vlog' }}</text>
              <text class="preview-title">{{ item.title }}</text>
            </view>
          </view>
        </view>
      </scroll-view>
    </view>
    <FloatingPublishButton />
  </view>
</template>

<script>
import { getHomeFeed } from '../../api/modules/home'
import { getPostPosterUrl, getPostVideoUrl, hasPostVideo } from '../../utils/post-media'
import { go } from '../../utils/navigation'
import FloatingPublishButton from '../../components/common/FloatingPublishButton.vue'

export default {
  components: {
    FloatingPublishButton
  },
  data() {
    return {
      heroImage: 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&q=80&w=2000',
      previewItems: []
    }
  },
  onLoad() {
    this.fetchFeed()
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
    async fetchFeed() {
      const result = await getHomeFeed()
      this.previewItems = result.list
    },
    goStrategyForm() {
      go('/pages/strategy-form/index')
    },
    goMatch() {
      go('/pages/match/index')
    },
    goSearch(keyword) {
      go(`/pages/search-result/index?keyword=${keyword}&type=all`)
    },
    goStrategyList() {
      uni.switchTab({
        url: '/pages/strategy-list/index'
      })
    },
    openPreview(item) {
      if (item.contentType === 'strategy') {
        go(`/pages/strategy-detail/index?id=${item.id}`)
        return
      }
      go(`/pages/vlog-detail/index?id=${item.id}`)
    }
  }
}
</script>

<style scoped lang="scss">
.home-page {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  padding-bottom: 220rpx;
}

.hero-bg,
.hero-mask {
  position: absolute;
  inset: 0;
}

.hero-bg {
  width: 100%;
  height: 76vh;
}

.hero-mask {
  background: linear-gradient(180deg, rgba(7, 17, 31, 0.12) 0%, rgba(7, 17, 31, 0.24) 52%, #07111f 100%);
}

.hero-content {
  position: relative;
  z-index: 2;
  padding: 120rpx 36rpx 0;
}

.heading {
  margin-top: 360rpx;
}

.hero-title {
  display: block;
  margin-top: 22rpx;
  width: 74%;
  font-size: 58rpx;
  line-height: 1.15;
  font-weight: 700;
  color: #f6f0e8;
}

.cta-row {
  display: flex;
  gap: 20rpx;
  margin-top: 34rpx;
}

.cta {
  min-width: 180rpx;
}

.search-box {
  margin-top: 42rpx;
  height: 108rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  padding: 0 34rpx;
}

.search-icon,
.search-divider {
  color: rgba(246, 240, 232, 0.5);
  font-size: 28rpx;
}

.search-divider {
  margin-left: auto;
  margin-right: 22rpx;
}

.search-placeholder {
  margin-left: 18rpx;
  color: rgba(246, 240, 232, 0.72);
  font-size: 28rpx;
}

.preview-panel {
  position: relative;
  z-index: 3;
  margin: 92rpx 24rpx 0;
  border-radius: 34rpx;
  padding: 28rpx;
}

.preview-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.preview-link {
  font-size: 24rpx;
  color: #ecd6b3;
}

.preview-scroll {
  margin-top: 24rpx;
  white-space: nowrap;
}

.preview-row {
  display: inline-flex;
  gap: 18rpx;
}

.preview-card {
  position: relative;
  width: 280rpx;
  height: 340rpx;
  border-radius: 26rpx;
  overflow: hidden;
}

.preview-image,
.preview-mask {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.preview-mask {
  background: linear-gradient(180deg, rgba(7, 17, 31, 0.1) 15%, rgba(7, 17, 31, 0.78) 100%);
}

.preview-text {
  position: absolute;
  left: 22rpx;
  right: 22rpx;
  bottom: 20rpx;
}

.preview-type {
  display: block;
  font-size: 20rpx;
  letter-spacing: 4rpx;
  color: rgba(246, 240, 232, 0.5);
}

.preview-title {
  display: block;
  margin-top: 10rpx;
  white-space: normal;
  font-size: 28rpx;
  line-height: 1.4;
  color: #f6f0e8;
  font-weight: 700;
}
</style>
