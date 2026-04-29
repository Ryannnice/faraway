<template>
  <view class="vlog-page">
    <view class="back-float" @tap="handleBack">‹</view>
    <swiper class="vlog-swiper" vertical circular :current="currentIndex" @change="handleSwipe">
      <swiper-item v-for="item in list" :key="item.id">
        <view class="vlog-item">
          <video
            v-if="hasVideo(item)"
            class="vlog-cover"
            :src="getVideoUrl(item)"
            :poster="getPosterUrl(item)"
            object-fit="cover"
            autoplay
            loop
            controls
          />
          <image v-else class="vlog-cover" :src="item.coverUrl" mode="aspectFill" />
          <view class="vlog-mask" />
          <view class="top-fade" />

          <view class="right-rail">
            <view class="author-rail" @tap.stop="openAuthor(item.author.id)">
              <image class="rail-avatar" :src="item.author.avatar" mode="aspectFill" />
              <view class="follow-pill">主页</view>
            </view>

            <view class="rail-action" @tap.stop="toggleLike(item)">
              <view class="rail-icon-circle">
                <text class="rail-icon">{{ item.isLiked ? '♥' : '♡' }}</text>
              </view>
              <text class="rail-count">{{ item.likeCount }}</text>
              <text class="rail-label">点赞</text>
            </view>

            <view class="rail-action" @tap.stop="toggleFavorite(item)">
              <view class="rail-icon-circle">
                <text class="rail-icon">{{ item.isFavorited ? '★' : '☆' }}</text>
              </view>
              <text class="rail-count">{{ item.favoriteCount }}</text>
              <text class="rail-label">收藏</text>
            </view>

            <view class="rail-action" @tap.stop="openCommentInput">
              <view class="rail-icon-circle">
                <text class="rail-icon">✎</text>
              </view>
              <text class="rail-count">{{ item.commentCount }}</text>
              <text class="rail-label">评论</text>
            </view>

            <view class="rail-action" @tap.stop="shareItem(item)">
              <view class="rail-icon-circle">
                <text class="rail-icon">⇪</text>
              </view>
              <text class="rail-count">{{ item.shareCount }}</text>
              <text class="rail-label">分享</text>
            </view>
          </view>

          <view class="vlog-body">
            <view v-if="item.location" class="location-chip">
              <text class="chip-icon">◎</text>
              <text class="chip-text">{{ item.location }}</text>
            </view>
            <view class="author-row" @tap="openAuthor(item.author.id)">
              <image class="body-avatar" :src="item.author.avatar" mode="aspectFill" />
              <text class="author-handle">@{{ item.author.nickname }}</text>
            </view>
            <text class="vlog-title">{{ item.title || '未命名 Vlog' }}</text>
            <text class="vlog-desc">{{ item.content || '这个瞬间值得被记录。' }}</text>
          </view>
        </view>
      </swiper-item>
    </swiper>

    <view v-if="currentItem" class="comment-sheet glass-card">
      <view class="comment-input-row">
        <input v-model="commentText" class="comment-input" placeholder="说点什么..." placeholder-style="color: rgba(246,240,232,0.24)" />
        <view class="send-btn" @tap="submitComment">发送</view>
      </view>
      <view class="comment-list">
        <view v-for="item in comments" :key="item.id" class="comment-item">
          <image class="comment-avatar" :src="item.avatar" mode="aspectFill" />
          <view class="comment-body">
            <text class="comment-name">{{ item.nickname }}</text>
            <text class="comment-content">{{ item.content }}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { createPostComment, getPostComments, getPostDetail, getPostList, sharePost, togglePostFavorite, togglePostLike } from '../../api/modules/post'
import { getPostPosterUrl, getPostVideoUrl, hasPostVideo } from '../../utils/post-media'
import { go, safeBack } from '../../utils/navigation'

export default {
  data() {
    return {
      list: [],
      currentIndex: 0,
      comments: [],
      commentText: '',
      fromPublish: false,
      currentId: ''
    }
  },
  async onLoad(options) {
    this.currentId = options && options.id ? String(options.id) : ''
    this.fromPublish = !!(options && String(options.fromPublish) === '1')
    await this.loadFeed()
    await this.loadComments()
  },
  computed: {
    currentItem() {
      return this.list[this.currentIndex] || null
    }
  },
  methods: {
    safeBack,
    async loadFeed() {
      const result = await getPostList()
      const items = Array.isArray(result.list) ? result.list : []

      if (!this.currentId) {
        this.list = items
        this.currentIndex = 0
        return
      }

      const foundIndex = items.findIndex((item) => String(item.id) === this.currentId)
      if (foundIndex >= 0) {
        this.list = items
        this.currentIndex = foundIndex
        return
      }

      const detail = await getPostDetail(this.currentId)
      this.list = detail ? [detail, ...items.filter((item) => String(item.id) !== this.currentId)] : items
      this.currentIndex = 0
    },
    handleBack() {
      if (this.fromPublish) {
        uni.reLaunch({
          url: '/pages/vlog-list/index'
        })
        return
      }
      this.safeBack('/pages/vlog-list/index')
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
    openAuthor(userId) {
      go(`/pages/user-profile/index?userId=${userId}`)
    },
    async loadComments() {
      if (!this.currentItem) {
        this.comments = []
        return
      }
      const result = await getPostComments(this.currentItem.id)
      this.comments = result.list
    },
    async handleSwipe(event) {
      this.currentIndex = event.detail.current
      await this.loadComments()
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
    openCommentInput() {
      uni.showToast({
        title: '在底部输入评论',
        icon: 'none'
      })
    },
    async submitComment() {
      if (!this.currentItem || !this.commentText) {
        return
      }
      await createPostComment(this.currentItem.id, {
        content: this.commentText
      })
      this.commentText = ''
      await this.loadComments()
      this.currentItem.commentCount = this.comments.length
    },
    async shareItem(item) {
      const result = await sharePost(item.id)
      item.shareCount = result.shareCount
      uni.showToast({
        title: '分享成功',
        icon: 'none'
      })
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

.back-float {
  position: fixed;
  top: 84rpx;
  left: 24rpx;
  z-index: 6;
  width: 76rpx;
  height: 76rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.08);
  color: #f6f0e8;
  font-size: 42rpx;
}

.vlog-swiper {
  height: 100vh;
}

.vlog-item {
  position: relative;
  height: 100%;
  overflow: hidden;
}

.vlog-cover,
.vlog-mask {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.vlog-mask {
  background:
    linear-gradient(180deg, rgba(0, 0, 0, 0.12) 0%, rgba(0, 0, 0, 0.16) 24%, rgba(0, 0, 0, 0.2) 50%, rgba(0, 0, 0, 0.65) 88%, rgba(0, 0, 0, 0.88) 100%);
}

.top-fade {
  position: absolute;
  inset: 0 0 auto 0;
  height: 240rpx;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.26) 0%, rgba(0, 0, 0, 0) 100%);
  z-index: 1;
}

.right-rail {
  position: absolute;
  right: 24rpx;
  bottom: 290rpx;
  z-index: 4;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 26rpx;
}

.author-rail {
  width: 100rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.rail-avatar,
.body-avatar,
.comment-avatar {
  border-radius: 50%;
}

.rail-avatar {
  width: 90rpx;
  height: 90rpx;
  border: 4rpx solid rgba(255, 255, 255, 0.45);
}

.follow-pill {
  margin-top: -10rpx;
  min-width: 60rpx;
  padding: 10rpx 14rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.92);
  color: #111111;
  font-size: 22rpx;
  font-weight: 700;
  text-align: center;
}

.rail-action {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.rail-icon-circle {
  width: 92rpx;
  height: 92rpx;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.18);
  backdrop-filter: blur(10rpx);
  display: flex;
  align-items: center;
  justify-content: center;
}

.rail-icon {
  font-size: 44rpx;
  color: #ffffff;
}

.rail-count,
.rail-label {
  margin-top: 10rpx;
  color: rgba(255, 255, 255, 0.96);
}

.rail-count {
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
  bottom: 240rpx;
  z-index: 4;
}

.location-chip {
  display: inline-flex;
  align-items: center;
  gap: 10rpx;
  min-height: 68rpx;
  padding: 0 24rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.18);
  backdrop-filter: blur(10rpx);
}

.chip-icon,
.chip-text,
.author-handle,
.vlog-title,
.vlog-desc {
  display: block;
}

.chip-icon {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.82);
}

.chip-text {
  font-size: 22rpx;
  color: rgba(255, 255, 255, 0.92);
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

.vlog-title {
  margin-top: 18rpx;
  font-size: 56rpx;
  line-height: 1.1;
  font-weight: 700;
  color: #ffffff;
}

.vlog-desc {
  margin-top: 18rpx;
  font-size: 28rpx;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.84);
}

.comment-sheet {
  position: fixed;
  left: 24rpx;
  right: 24rpx;
  bottom: 38rpx;
  z-index: 5;
  border-radius: 28rpx;
  padding: 24rpx;
}

.comment-input-row {
  display: flex;
  gap: 16rpx;
}

.comment-input {
  flex: 1;
  height: 84rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.06);
  padding: 0 26rpx;
  color: #f6f0e8;
}

.send-btn {
  width: 120rpx;
  height: 84rpx;
  border-radius: 999rpx;
  background: #ecd6b3;
  color: #07111f;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  font-weight: 700;
}

.comment-list {
  margin-top: 18rpx;
  display: flex;
  flex-direction: column;
  gap: 14rpx;
  max-height: 220rpx;
  overflow: hidden;
}

.comment-item {
  display: flex;
}

.comment-avatar {
  width: 56rpx;
  height: 56rpx;
}

.comment-body {
  margin-left: 14rpx;
}

.comment-name {
  display: block;
  font-size: 22rpx;
  font-weight: 700;
}

.comment-content {
  display: block;
  margin-top: 6rpx;
  font-size: 22rpx;
  line-height: 1.6;
  color: rgba(246, 240, 232, 0.82);
}
</style>
