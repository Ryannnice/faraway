<template>
  <view class="vlog-page">
    <swiper class="vlog-swiper" vertical circular :current="currentIndex" @change="handleSwipe">
      <swiper-item v-for="(item, index) in list" :key="item.id">
        <view class="vlog-item">
          <video
            v-if="hasVideo(item)"
            :id="videoDomId(item.id)"
            class="vlog-cover"
            :src="getVideoUrl(item)"
            :poster="getPosterUrl(item)"
            object-fit="cover"
            :autoplay="index === currentIndex"
            muted
            loop
            :controls="false"
            :show-center-play-btn="false"
            :enable-progress-gesture="false"
            :show-play-btn="false"
          />
          <image v-else-if="getFeedCover(item)" class="vlog-cover" :src="getFeedCover(item)" mode="aspectFill" />
          <view v-else class="vlog-fallback">
            <text class="fallback-kicker">VLOG</text>
            <text class="fallback-title">{{ item.title || '点击进入详情' }}</text>
          </view>

          <cover-view class="top-layer">
            <cover-view class="search-float" @tap="openSearch">
              <cover-view class="search-icon">⌕</cover-view>
              <cover-view class="search-label">搜索标签、城市...</cover-view>
            </cover-view>

            <cover-view class="vlog-mask" />
            <cover-view class="top-fade" />

            <cover-view class="right-rail">
              <cover-view class="author-rail" @tap="openAuthor(item.author.id)">
                <cover-image class="rail-avatar" :src="item.author.avatar || defaultAvatar" />
                <cover-view class="follow-pill">主页</cover-view>
              </cover-view>

              <cover-view class="rail-action" @tap="toggleLike(item)">
                <cover-view class="rail-icon-circle">
                  <cover-view class="rail-icon">{{ item.isLiked ? '♥' : '♡' }}</cover-view>
                </cover-view>
                <cover-view class="rail-count">{{ item.likeCount }}</cover-view>
                <cover-view class="rail-label">点赞</cover-view>
              </cover-view>

              <cover-view class="rail-action" @tap="toggleFavorite(item)">
                <cover-view class="rail-icon-circle">
                  <cover-view class="rail-icon">{{ item.isFavorited ? '★' : '☆' }}</cover-view>
                </cover-view>
                <cover-view class="rail-count">{{ item.favoriteCount }}</cover-view>
                <cover-view class="rail-label">收藏</cover-view>
              </cover-view>

              <cover-view class="rail-action" @tap="openDetail(item.id)">
                <cover-view class="rail-icon-circle">
                  <cover-view class="rail-icon">✎</cover-view>
                </cover-view>
                <cover-view class="rail-count">{{ item.commentCount }}</cover-view>
                <cover-view class="rail-label">评论</cover-view>
              </cover-view>

              <cover-view class="rail-action" @tap="shareItem(item)">
                <cover-view class="rail-icon-circle">
                  <cover-view class="rail-icon">⇪</cover-view>
                </cover-view>
                <cover-view class="rail-count">{{ item.shareCount }}</cover-view>
                <cover-view class="rail-label">分享</cover-view>
              </cover-view>

              <cover-view class="rail-action rail-action-next" @tap="goNext">
                <cover-view class="rail-icon-circle rail-icon-circle-next">
                  <cover-view class="rail-icon">↓</cover-view>
                </cover-view>
                <cover-view class="rail-label">下一条</cover-view>
              </cover-view>
            </cover-view>

            <cover-view class="vlog-body">
              <cover-view v-if="item.location" class="location-chip">
                <cover-view class="chip-icon">◎</cover-view>
                <cover-view class="chip-text">{{ item.location }}</cover-view>
              </cover-view>

              <cover-view class="author-row" @tap="openAuthor(item.author.id)">
                <cover-image class="body-avatar" :src="item.author.avatar || defaultAvatar" />
                <cover-view class="author-handle">@{{ item.author.nickname || 'Faraway' }}</cover-view>
              </cover-view>

              <cover-view class="vlog-title">{{ item.title || '未命名 Vlog' }}</cover-view>
              <cover-view class="vlog-desc">{{ item.content || '这个瞬间值得被记录。' }}</cover-view>
              <cover-view class="detail-pill" @tap="openDetail(item.id)">查看详情</cover-view>
            </cover-view>
          </cover-view>
        </view>
      </swiper-item>
    </swiper>

    <FloatingPublishButton />
  </view>
</template>

<script>
import { getPostList, sharePost, togglePostFavorite, togglePostLike } from '../../api/modules/post'
import { getPostPosterUrl, getPostVideoUrl, hasPostVideo, isVideoLikeUrl } from '../../utils/post-media'
import { go } from '../../utils/navigation'
import FloatingPublishButton from '../../components/common/FloatingPublishButton.vue'

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
  components: {
    FloatingPublishButton
  },
  data() {
    return {
      list: [],
      currentIndex: 0,
      defaultAvatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=400'
    }
  },
  async onLoad() {
    await this.fetchList()
  },
  methods: {
    videoDomId(id) {
      return `vlog-video-${id}`
    },
    hasVideo(item) {
      return hasPostVideo(item)
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
    getVideoUrl(item) {
      return getPostVideoUrl(item)
    },
    getPosterUrl(item) {
      return getPostPosterUrl(item)
    },
    async fetchList() {
      const result = await getPostList()
      this.list = shuffleItems(result.list || [])
      this.currentIndex = 0
      this.$nextTick(() => {
        this.syncPlayback()
      })
    },
    openAuthor(userId) {
      go(`/pages/user-profile/index?userId=${userId}`)
    },
    openSearch() {
      go('/pages/search-result/index?keyword=&type=vlog')
    },
    async handleSwipe(event) {
      const previousIndex = this.currentIndex
      this.pauseVideoByIndex(previousIndex)
      this.currentIndex = event.detail.current
      if (this.list.length > 1 && previousIndex === this.list.length - 1 && this.currentIndex === 0) {
        await this.fetchList()
        return
      }
      this.$nextTick(() => {
        this.syncPlayback()
      })
    },
    pauseVideoByIndex(index) {
      const item = this.list[index]
      if (!item || !this.hasVideo(item)) {
        return
      }
      const ctx = uni.createVideoContext(this.videoDomId(item.id), this)
      ctx.pause()
    },
    playVideoByIndex(index) {
      const item = this.list[index]
      if (!item || !this.hasVideo(item)) {
        return
      }
      const ctx = uni.createVideoContext(this.videoDomId(item.id), this)
      ctx.play()
    },
    syncPlayback() {
      this.list.forEach((item, index) => {
        if (!this.hasVideo(item)) {
          return
        }
        if (index === this.currentIndex) {
          this.playVideoByIndex(index)
          return
        }
        this.pauseVideoByIndex(index)
      })
    },
    async goNext() {
      if (!this.list.length) {
        return
      }
      if (this.list.length === 1) {
        uni.showToast({
          title: '暂时没有下一条了',
          icon: 'none'
        })
        return
      }
      const nextIndex = (this.currentIndex + 1) % this.list.length
      const reordered = [
        ...this.list.slice(nextIndex),
        ...this.list.slice(0, nextIndex)
      ]
      this.pauseVideoByIndex(this.currentIndex)
      this.list = reordered
      this.currentIndex = 0
      this.$nextTick(() => {
        this.syncPlayback()
      })
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
  height: 100vh;
  overflow: hidden;
  background: #0a0d12;
}

.vlog-swiper {
  height: 100vh;
}

.vlog-item {
  position: relative;
  height: 100%;
  overflow: hidden;
  background: #0a0d12;
}

.vlog-cover,
.vlog-fallback {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.vlog-fallback {
  padding: 34rpx;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  background:
    radial-gradient(circle at top left, rgba(236, 214, 179, 0.22), transparent 38%),
    linear-gradient(160deg, #163047 0%, #0d1825 52%, #09111a 100%);
}

.top-layer {
  position: absolute;
  inset: 0;
}

.search-float {
  position: absolute;
  top: 92rpx;
  left: 48rpx;
  right: 48rpx;
  z-index: 6;
  height: 92rpx;
  border-radius: 999rpx;
  padding: 0 30rpx;
  display: flex;
  align-items: center;
  background: rgba(39, 44, 51, 0.58);
  border: 2rpx solid rgba(255, 255, 255, 0.08);
}

.search-icon {
  font-size: 34rpx;
  color: rgba(255, 255, 255, 0.62);
}

.search-label {
  margin-left: 18rpx;
  color: rgba(255, 255, 255, 0.44);
  font-size: 26rpx;
}

.vlog-mask {
  position: absolute;
  inset: 0;
  z-index: 2;
  background:
    linear-gradient(180deg, rgba(0, 0, 0, 0.12) 0%, rgba(0, 0, 0, 0.18) 18%, rgba(0, 0, 0, 0.18) 42%, rgba(0, 0, 0, 0.62) 88%, rgba(0, 0, 0, 0.86) 100%);
}

.top-fade {
  position: absolute;
  inset: 0 0 auto 0;
  height: 320rpx;
  z-index: 3;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.28) 0%, rgba(0, 0, 0, 0) 100%);
}

.right-rail {
  position: absolute;
  right: 24rpx;
  bottom: 310rpx;
  z-index: 5;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 28rpx;
}

.author-rail {
  width: 96rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.rail-avatar,
.body-avatar {
  border-radius: 50%;
}

.rail-avatar {
  width: 88rpx;
  height: 88rpx;
}

.follow-pill {
  margin-top: -8rpx;
  min-width: 56rpx;
  padding: 10rpx 14rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.92);
  color: #101010;
  font-size: 22rpx;
  font-weight: 700;
  text-align: center;
}

.rail-action {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.rail-action-next {
  margin-top: 8rpx;
}

.rail-icon-circle {
  width: 92rpx;
  height: 92rpx;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.18);
  display: flex;
  align-items: center;
  justify-content: center;
}

.rail-icon-circle-next {
  background: rgba(255, 255, 255, 0.26);
}

.rail-icon {
  font-size: 44rpx;
  color: #ffffff;
}

.rail-count,
.rail-label {
  color: rgba(255, 255, 255, 0.96);
  text-align: center;
}

.rail-count {
  margin-top: 12rpx;
  font-size: 24rpx;
  font-weight: 700;
}

.rail-label {
  margin-top: 4rpx;
  font-size: 22rpx;
}

.vlog-body {
  position: absolute;
  left: 34rpx;
  right: 152rpx;
  bottom: 180rpx;
  z-index: 5;
}

.location-chip {
  display: inline-flex;
  align-items: center;
  gap: 10rpx;
  min-height: 68rpx;
  padding: 0 24rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.18);
}

.chip-icon,
.chip-text,
.author-handle,
.vlog-title,
.vlog-desc,
.fallback-kicker,
.fallback-title {
  display: block;
}

.chip-icon {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.82);
}

.chip-text {
  font-size: 22rpx;
  color: rgba(255, 255, 255, 0.9);
}

.author-row {
  margin-top: 26rpx;
  display: flex;
  align-items: center;
}

.body-avatar {
  width: 56rpx;
  height: 56rpx;
}

.author-handle {
  margin-left: 14rpx;
  font-size: 28rpx;
  font-weight: 700;
  color: #ffffff;
}

.vlog-title,
.fallback-title {
  margin-top: 18rpx;
  font-size: 56rpx;
  line-height: 1.1;
  font-weight: 700;
  color: #ffffff;
}

.fallback-kicker {
  font-size: 20rpx;
  letter-spacing: 4rpx;
  color: rgba(255, 255, 255, 0.56);
}

.vlog-desc {
  margin-top: 18rpx;
  font-size: 28rpx;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.84);
}

.detail-pill {
  margin-top: 26rpx;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 180rpx;
  height: 72rpx;
  padding: 0 26rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.16);
  color: #ffffff;
  font-size: 24rpx;
  font-weight: 700;
}
</style>
