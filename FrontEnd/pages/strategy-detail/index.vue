<template>
  <view v-if="detail" class="page-shell">
    <AppHeader title="攻略详情" subtitle="Strategy Detail" :fallback="fallback" :force-fallback="fromPublish" />
    <view v-if="galleryImages.length" class="hero-gallery">
      <image
        class="hero-image"
        :src="galleryImages[0]"
        mode="widthFix"
        @tap="previewImages(0)"
      />
      <view v-if="galleryImages.length > 1" class="hero-hint">点击图片查看大图</view>
    </view>
    <view class="meta-panel">
      <text class="section-kicker">{{ detail.destination }}</text>
      <text class="section-title detail-title">{{ detail.title }}</text>
      <text class="detail-summary">{{ detail.summary }}</text>
      <view class="tag-row">
        <text v-for="tag in detail.tags" :key="tag" class="tag-chip">{{ tag }}</text>
      </view>
    </view>

    <view class="author-card glass-card" @tap="openAuthor">
      <image class="author-avatar" :src="detail.author.avatar" mode="aspectFill" />
      <view class="author-text">
        <text class="author-name">{{ detail.author.nickname }}</text>
        <text class="author-bio">点击查看作者主页</text>
      </view>
    </view>

    <view class="action-bar glass-card">
      <view class="action-item" @tap="handleLike">
        <text class="action-icon">{{ detail.isLiked ? '♥' : '♡' }}</text>
        <text class="action-label">点赞 {{ detail.likeCount }}</text>
      </view>
      <view class="action-item" @tap="handleFavorite">
        <text class="action-icon">{{ detail.isFavorited ? '★' : '☆' }}</text>
        <text class="action-label">收藏 {{ detail.favoriteCount }}</text>
      </view>
      <view class="action-item" @tap="focusComment">
        <text class="action-icon">✎</text>
        <text class="action-label">评论 {{ detail.commentCount }}</text>
      </view>
      <view class="action-item" @tap="handleShare">
        <text class="action-icon">⇪</text>
        <text class="action-label">分享 {{ detail.shareCount }}</text>
      </view>
    </view>

    <view v-if="detail.content" class="content-block glass-card">
      <text class="content-text">{{ detail.content }}</text>
    </view>

    <view v-if="extraGalleryImages.length" class="gallery-block">
      <image
        v-for="(item, index) in extraGalleryImages"
        :key="item + index"
        class="gallery-image"
        :src="item"
        mode="widthFix"
        @tap="previewImages(index + 1)"
      />
    </view>

    <view class="stat-row glass-card">
      <text>浏览 {{ detail.viewCount }}</text>
      <text>点赞 {{ detail.likeCount }}</text>
      <text>收藏 {{ detail.favoriteCount }}</text>
    </view>

    <view class="comment-card glass-card">
      <text class="comment-title">评论区</text>
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
            <text class="comment-time">{{ item.createdAt }}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import AppHeader from '../../components/common/AppHeader.vue'
import {
  createStrategyComment,
  getStrategyComments,
  getStrategyDetail,
  shareStrategy,
  toggleStrategyFavorite,
  toggleStrategyLike
} from '../../api/modules/strategy'
import { go } from '../../utils/navigation'

export default {
  components: {
    AppHeader
  },
  data() {
    return {
      detail: null,
      fallback: '/pages/strategy-list/index',
      fromPublish: false,
      commentText: '',
      comments: [],
      strategyId: ''
    }
  },
  computed: {
    galleryImages() {
      if (!this.detail) {
        return []
      }
      const images = Array.isArray(this.detail.imageList) ? this.detail.imageList : []
      const normalized = images
        .map((item) => {
          if (typeof item === 'string') {
            return item
          }
          return item && item.url ? item.url : ''
        })
        .filter(Boolean)
      if (normalized.length) {
        return normalized
      }
      return this.detail.coverUrl ? [this.detail.coverUrl] : []
    },
    extraGalleryImages() {
      return this.galleryImages.slice(1)
    }
  },
  async onLoad(options) {
    this.strategyId = options && options.id
    this.fromPublish = !!(options && String(options.fromPublish) === '1')
    await this.refreshDetail()
    this.loadComments()
  },
  methods: {
    async refreshDetail() {
      this.detail = await getStrategyDetail(this.strategyId)
    },
    async loadComments() {
      const result = await getStrategyComments(this.strategyId)
      this.comments = result.list
    },
    openAuthor() {
      go(`/pages/user-profile/index?userId=${this.detail.author.id}`)
    },
    async handleLike() {
      const result = await toggleStrategyLike(this.strategyId)
      this.detail.isLiked = result.isLiked
      this.detail.likeCount = result.likeCount
    },
    async handleFavorite() {
      const result = await toggleStrategyFavorite(this.strategyId)
      this.detail.isFavorited = result.isFavorited
      this.detail.favoriteCount = result.favoriteCount
    },
    async handleShare() {
      const result = await shareStrategy(this.strategyId)
      this.detail.shareCount = result.shareCount
      uni.showToast({
        title: '分享成功',
        icon: 'none'
      })
    },
    focusComment() {
      uni.showToast({
        title: '在下方输入评论',
        icon: 'none'
      })
    },
    previewImages(index = 0) {
      if (!this.galleryImages.length) {
        return
      }
      uni.previewImage({
        current: this.galleryImages[index] || this.galleryImages[0],
        urls: this.galleryImages
      })
    },
    async submitComment() {
      if (!this.commentText) {
        return
      }
      await createStrategyComment(this.strategyId, {
        content: this.commentText
      })
      this.commentText = ''
      await this.loadComments()
      this.detail.commentCount = this.comments.length
    }
  }
}
</script>

<style scoped lang="scss">
.hero-gallery {
  margin-top: 8rpx;
}

.hero-image {
  width: 100%;
  border-radius: 34rpx;
}

.hero-hint {
  margin-top: 14rpx;
  font-size: 22rpx;
  color: rgba(246, 240, 232, 0.45);
  text-align: center;
}

.meta-panel {
  margin-top: 30rpx;
}

.detail-title {
  margin-top: 14rpx;
}

.detail-summary,
.content-text {
  display: block;
  margin-top: 20rpx;
  font-size: 28rpx;
  line-height: 1.8;
  color: rgba(246, 240, 232, 0.72);
}

.tag-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
  margin-top: 20rpx;
}

.author-card,
.content-block,
.gallery-block,
.stat-row,
.action-bar,
.comment-card {
  margin-top: 28rpx;
  border-radius: 30rpx;
  padding: 28rpx;
}

.author-card {
  display: flex;
  align-items: center;
}

.author-avatar {
  width: 88rpx;
  height: 88rpx;
  border-radius: 50%;
}

.author-text {
  margin-left: 20rpx;
}

.author-name {
  display: block;
  font-size: 30rpx;
  font-weight: 700;
}

.author-bio {
  display: block;
  margin-top: 8rpx;
  font-size: 22rpx;
  color: rgba(246, 240, 232, 0.52);
}

.action-bar,
.stat-row {
  display: flex;
  justify-content: space-between;
  gap: 12rpx;
  font-size: 24rpx;
  color: rgba(246, 240, 232, 0.72);
}

.gallery-block {
  display: flex;
  flex-direction: column;
  gap: 18rpx;
}

.gallery-image {
  width: 100%;
  border-radius: 28rpx;
}

.action-item {
  flex: 1;
  text-align: center;
}

.action-icon,
.action-label,
.comment-title,
.comment-name,
.comment-content,
.comment-time {
  display: block;
}

.action-icon {
  font-size: 30rpx;
}

.action-label {
  margin-top: 10rpx;
  font-size: 22rpx;
}

.comment-title {
  font-size: 30rpx;
  font-weight: 700;
}

.comment-input-row {
  display: flex;
  gap: 16rpx;
  margin-top: 20rpx;
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
  margin-top: 24rpx;
  display: flex;
  flex-direction: column;
  gap: 18rpx;
}

.comment-item {
  display: flex;
}

.comment-avatar {
  width: 64rpx;
  height: 64rpx;
  border-radius: 50%;
}

.comment-body {
  margin-left: 16rpx;
}

.comment-name {
  font-size: 24rpx;
  font-weight: 700;
}

.comment-content {
  margin-top: 8rpx;
  font-size: 24rpx;
  line-height: 1.7;
}

.comment-time {
  margin-top: 8rpx;
  font-size: 20rpx;
  color: rgba(246, 240, 232, 0.45);
}
</style>
