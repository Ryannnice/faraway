<template>
  <view class="vlog-page">
    <view class="video-stage">
      <video
        v-if="currentItem && hasVideo(currentItem)"
        :id="videoDomId(currentItem.id)"
        :key="videoKey"
        class="main-video"
        :src="getVideoUrl(currentItem)"
        :poster="disablePoster ? '' : getPosterUrl(currentItem)"
        object-fit="contain"
        autoplay
        loop
        :muted="false"
        :controls="false"
        :show-center-play-btn="false"
        :show-play-btn="false"
        :enable-progress-gesture="true"
      />

      <view v-else class="video-fallback">
        <image
          v-if="currentItem && getFeedCover(currentItem)"
          class="fallback-image"
          :src="getFeedCover(currentItem)"
          mode="aspectFit"
        />
        <view v-else class="fallback-empty">
          <text class="fallback-title">{{ currentItem ? (currentItem.title || '暂无视频') : '暂无内容' }}</text>
        </view>
      </view>

      <view class="top-tools">
        <view class="search-btn" @tap="openSearch">搜索标签、城市...</view>
      </view>

      <view v-if="currentItem" class="side-actions">
        <view class="action-item" @tap="toggleLike(currentItem)">
          <text class="action-icon">{{ currentItem.isLiked ? '♥' : '♡' }}</text>
          <text class="action-text">{{ formatCount(currentItem.likeCount) }}</text>
        </view>
        <view class="action-item" @tap="toggleFavorite(currentItem)">
          <text class="action-icon">{{ currentItem.isFavorited ? '★' : '☆' }}</text>
          <text class="action-text">{{ formatCount(currentItem.favoriteCount) }}</text>
        </view>
        <view class="action-item" @tap="openDetail(currentItem.id)">
          <text class="action-icon">✎</text>
          <text class="action-text">{{ formatCount(currentItem.commentCount) }}</text>
        </view>
        <view class="action-item" @tap="shareItem(currentItem)">
          <text class="action-icon">⇪</text>
          <text class="action-text">{{ formatCount(currentItem.shareCount) }}</text>
        </view>
      </view>
    </view>

    <view v-if="currentItem" class="bottom-panel">
      <view class="author-row" @tap="openAuthor(currentItem.author.id)">
        <image class="author-avatar" :src="currentItem.author.avatar || defaultAvatar" mode="aspectFill" />
        <text class="author-name">@{{ currentItem.author.nickname || 'Faraway' }}</text>
      </view>

      <text class="video-title">{{ currentItem.title || '未命名 Vlog' }}</text>
      <text class="video-desc">{{ currentItem.content || '这个瞬间值得被记录。' }}</text>
      <text v-if="currentItem.location" class="video-meta">{{ currentItem.location }}</text>

      <view class="button-row">
        <view class="control-btn primary-btn" @tap="togglePlayback">
          {{ isPlaying ? '暂停' : '播放' }}
        </view>
        <view class="control-btn" @tap="playNext">下一条</view>
        <view class="control-btn" @tap="openDetail(currentItem.id)">详情</view>
      </view>
    </view>
  </view>
</template>

<script>
import { getPostList, sharePost, togglePostFavorite, togglePostLike } from '../../api/modules/post'
import { getPostPosterUrl, getPostVideoUrl, hasPostVideo, isVideoLikeUrl } from '../../utils/post-media'
import { go } from '../../utils/navigation'

function shuffleItems(list = []) {
  const next = [...list]
  for (let i = next.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1))
    const temp = next[i]
    next[i] = next[j]
    next[j] = temp
  }
  return next
}

export default {
  data() {
    return {
      list: [],
      currentIndex: 0,
      defaultAvatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=400',
      isPlaying: true,
      videoKey: 0,
      disablePoster: true
    }
  },
  computed: {
    currentItem() {
      return this.list[this.currentIndex] || null
    }
  },
  async onLoad() {
    await this.fetchList()
  },
  methods: {
    videoDomId(id) {
      return `vlog-video-${id}`
    },
    formatCount(value) {
      const count = Number(value || 0)
      if (count >= 10000) {
        return `${(count / 10000).toFixed(count >= 100000 ? 0 : 1).replace(/\.0$/, '')}w`
      }
      if (count >= 1000) {
        return `${(count / 1000).toFixed(count >= 10000 ? 0 : 1).replace(/\.0$/, '')}k`
      }
      return String(count)
    },
    hasVideo(item) {
      return hasPostVideo(item)
    },
    getVideoUrl(item) {
      return getPostVideoUrl(item)
    },
    getPosterUrl(item) {
      return getPostPosterUrl(item)
    },
    getFeedCover(item) {
      const posterUrl = this.getPosterUrl(item)
      if (posterUrl) {
        return posterUrl
      }
      if (item && item.coverUrl && !isVideoLikeUrl(item.coverUrl)) {
        return item.coverUrl
      }
      return ''
    },
    async fetchList() {
      const result = await getPostList()
      this.list = shuffleItems(result.list || [])
      this.currentIndex = 0
      this.videoKey += 1
      this.isPlaying = true
      this.$nextTick(() => {
        this.playCurrentVideo()
      })
    },
    getCurrentVideoContext() {
      if (!this.currentItem || !this.hasVideo(this.currentItem)) {
        return null
      }
      try {
        return uni.createVideoContext(this.videoDomId(this.currentItem.id), this)
      } catch (error) {
        console.warn('create video context failed', error)
        return null
      }
    },
    playCurrentVideo() {
      const ctx = this.getCurrentVideoContext()
      if (!ctx) {
        return
      }
      try {
        ctx.play()
        this.isPlaying = true
      } catch (error) {
        console.warn('play video failed', error)
      }
    },
    pauseCurrentVideo() {
      const ctx = this.getCurrentVideoContext()
      if (!ctx) {
        return
      }
      try {
        ctx.pause()
        this.isPlaying = false
      } catch (error) {
        console.warn('pause video failed', error)
      }
    },
    togglePlayback() {
      if (this.isPlaying) {
        this.pauseCurrentVideo()
        return
      }
      this.playCurrentVideo()
    },
    playNext() {
      if (!this.list.length) {
        return
      }
      this.currentIndex = (this.currentIndex + 1) % this.list.length
      this.videoKey += 1
      this.isPlaying = true
      this.$nextTick(() => {
        this.playCurrentVideo()
      })
    },
    openAuthor(userId) {
      go(`/pages/user-profile/index?userId=${userId}`)
    },
    openSearch() {
      go('/pages/search-result/index?keyword=&type=vlog')
    },
    async toggleLike(item) {
      const result = await togglePostLike(item.id)
      item.isLiked = result.isLiked
      item.likeCount = result.likeCount
    },
    async toggleFavorite(item) {
      const result = await togglePostFavorite(item.id)
      item.isFavorited = result.isFavorited
      item.favoriteCount = result.favoriteCount
    },
    async shareItem(item) {
      const result = await sharePost(item.id)
      item.shareCount = result.shareCount
      uni.showToast({
        title: '分享成功',
        icon: 'none'
      })
    },
    openDetail(id) {
      go(`/pages/vlog-detail/index?id=${id}`)
    }
  }
}
</script>

<style scoped lang="scss">
.vlog-page {
  position: fixed;
  inset: 0;
  background: #000;
  display: flex;
  flex-direction: column;
}

.video-stage {
  position: relative;
  flex: 1;
  background: #000;
}

.main-video,
.video-fallback,
.fallback-image,
.fallback-empty {
  width: 100%;
  height: 100%;
}

.main-video,
.video-fallback {
  display: block;
  background: #000;
}

.fallback-empty {
  display: flex;
  align-items: center;
  justify-content: center;
}

.fallback-title {
  color: #fff;
  font-size: 34rpx;
}

.top-tools {
  position: absolute;
  top: 76rpx;
  left: 24rpx;
  right: 24rpx;
  z-index: 3;
  display: flex;
  justify-content: flex-start;
}

.search-btn {
  min-width: 360rpx;
  max-width: 520rpx;
  height: 76rpx;
  padding: 0 28rpx;
  border-radius: 999rpx;
  background: rgba(0, 0, 0, 0.42);
  color: rgba(255, 255, 255, 0.9);
  font-size: 26rpx;
  display: flex;
  align-items: center;
}

.side-actions {
  position: absolute;
  right: 18rpx;
  bottom: 60rpx;
  z-index: 3;
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.action-item {
  width: 92rpx;
  min-height: 92rpx;
  padding: 10rpx 0;
  border-radius: 22rpx;
  background: rgba(0, 0, 0, 0.36);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.action-icon {
  color: #fff;
  font-size: 40rpx;
  line-height: 1;
}

.action-text {
  margin-top: 8rpx;
  color: #fff;
  font-size: 20rpx;
}

.bottom-panel {
  padding: 24rpx 24rpx calc(24rpx + env(safe-area-inset-bottom));
  background: #0b0b0b;
}

.author-row {
  display: flex;
  align-items: center;
}

.author-avatar {
  width: 56rpx;
  height: 56rpx;
  border-radius: 50%;
}

.author-name {
  margin-left: 14rpx;
  color: #fff;
  font-size: 28rpx;
  font-weight: 700;
}

.video-title {
  display: block;
  margin-top: 16rpx;
  color: #fff;
  font-size: 42rpx;
  font-weight: 700;
  line-height: 1.2;
}

.video-desc {
  display: block;
  margin-top: 12rpx;
  color: rgba(255, 255, 255, 0.88);
  font-size: 26rpx;
  line-height: 1.5;
}

.video-meta {
  display: block;
  margin-top: 10rpx;
  color: rgba(255, 255, 255, 0.7);
  font-size: 22rpx;
}

.button-row {
  margin-top: 20rpx;
  display: flex;
  gap: 16rpx;
}

.control-btn {
  flex: 1;
  height: 76rpx;
  border-radius: 999rpx;
  background: #232323;
  color: #fff;
  font-size: 26rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.primary-btn {
  background: #ffffff;
  color: #111111;
  font-weight: 700;
}
</style>
