<template>
  <view class="vlog-page">
    <view class="back-float" @tap="safeBack('/pages/vlog-list/index')">‹</view>
    <swiper class="vlog-swiper" vertical circular :current="currentIndex" @change="handleSwipe">
      <swiper-item v-for="item in list" :key="item.id">
        <view class="vlog-item">
          <image class="vlog-cover" :src="item.coverUrl" mode="aspectFill" />
          <view class="vlog-mask" />
          <view class="vlog-meta" @tap="openAuthor(item.author.id)">
            <image class="author-avatar" :src="item.author.avatar" mode="aspectFill" />
            <view>
              <text class="author-name">{{ item.author.nickname }}</text>
              <text class="author-hint">查看作者主页</text>
            </view>
          </view>
          <view class="vlog-body">
            <text class="vlog-location">{{ item.location }}</text>
            <text class="vlog-title">{{ item.title }}</text>
            <text class="vlog-desc">{{ item.content }}</text>
            <view class="vlog-action-bar glass-card">
              <view class="vlog-action" @tap.stop="toggleLike(item)">
                <text>{{ item.isLiked ? '♥' : '♡' }}</text>
                <text>{{ item.likeCount }}</text>
              </view>
              <view class="vlog-action" @tap.stop="toggleFavorite(item)">
                <text>{{ item.isFavorited ? '★' : '☆' }}</text>
                <text>{{ item.favoriteCount }}</text>
              </view>
              <view class="vlog-action" @tap.stop="openCommentInput">
                <text>✎</text>
                <text>{{ item.commentCount }}</text>
              </view>
              <view class="vlog-action" @tap.stop="shareItem(item)">
                <text>⇪</text>
                <text>{{ item.shareCount }}</text>
              </view>
            </view>
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
import { createPostComment, getPostComments, getPostList, sharePost, togglePostFavorite, togglePostLike } from '../../api/modules/post'
import { go, safeBack } from '../../utils/navigation'

export default {
  data() {
    return {
      list: [],
      currentIndex: 0,
      comments: [],
      commentText: ''
    }
  },
  async onLoad(options) {
    const result = await getPostList()
    this.list = result.list
    const index = this.list.findIndex((item) => String(item.id) === String(options && options.id))
    this.currentIndex = index >= 0 ? index : 0
    this.loadComments()
  },
  computed: {
    currentItem() {
      return this.list[this.currentIndex] || null
    }
  },
  methods: {
    safeBack,
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
    handleSwipe(event) {
      this.currentIndex = event.detail.current
      this.loadComments()
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
  min-height: 100vh;
  background: #050c16;
}

.back-float {
  position: fixed;
  top: 80rpx;
  left: 24rpx;
  z-index: 5;
  width: 72rpx;
  height: 72rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.08);
  color: #f6f0e8;
  font-size: 40rpx;
}

.vlog-swiper {
  height: 100vh;
}

.vlog-item {
  position: relative;
  height: 100vh;
}

.vlog-cover,
.vlog-mask {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.vlog-mask {
  background: linear-gradient(180deg, rgba(7, 17, 31, 0.14) 0%, rgba(7, 17, 31, 0.24) 40%, rgba(7, 17, 31, 0.92) 100%);
}

.vlog-meta {
  position: absolute;
  top: 170rpx;
  left: 28rpx;
  display: flex;
  align-items: center;
  z-index: 2;
}

.author-avatar {
  width: 82rpx;
  height: 82rpx;
  border-radius: 50%;
}

.author-name,
.author-hint {
  display: block;
  margin-left: 18rpx;
}

.author-name {
  font-size: 28rpx;
  font-weight: 700;
}

.author-hint {
  margin-top: 8rpx;
  font-size: 22rpx;
  color: rgba(246, 240, 232, 0.56);
}

.vlog-body {
  position: absolute;
  left: 28rpx;
  right: 28rpx;
  bottom: 300rpx;
}

.vlog-location {
  display: block;
  font-size: 22rpx;
  letter-spacing: 4rpx;
  color: rgba(246, 240, 232, 0.56);
}

.vlog-title {
  display: block;
  margin-top: 16rpx;
  font-size: 46rpx;
  line-height: 1.2;
  font-weight: 700;
}

.vlog-desc {
  display: block;
  margin-top: 16rpx;
  width: 80%;
  font-size: 26rpx;
  line-height: 1.7;
  color: rgba(246, 240, 232, 0.74);
}

.vlog-action-bar {
  margin-top: 26rpx;
  display: flex;
  justify-content: space-between;
  padding: 22rpx 20rpx;
  border-radius: 24rpx;
}

.vlog-action {
  width: 25%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
  color: #f6f0e8;
  font-size: 22rpx;
}

.comment-sheet {
  position: fixed;
  left: 24rpx;
  right: 24rpx;
  bottom: 40rpx;
  z-index: 3;
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
}

.comment-item {
  display: flex;
}

.comment-avatar {
  width: 52rpx;
  height: 52rpx;
  border-radius: 50%;
}

.comment-body {
  margin-left: 14rpx;
}

.comment-name,
.comment-content {
  display: block;
}

.comment-name {
  font-size: 22rpx;
  font-weight: 700;
}

.comment-content {
  margin-top: 6rpx;
  font-size: 22rpx;
  color: rgba(246, 240, 232, 0.72);
}
</style>
