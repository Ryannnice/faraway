<template>
  <view class="vlog-page">
    <view class="search-float" @tap="openSearch">
      <text class="search-icon">⌕</text>
      <text class="search-label">搜索标签、城市...</text>
    </view>
    <swiper class="vlog-swiper" vertical circular>
      <swiper-item v-for="item in list" :key="item.id">
        <view class="vlog-item">
          <image class="vlog-cover" :src="item.coverUrl" mode="aspectFill" />
          <view class="vlog-mask" />
          <view class="top-fade" />

          <view class="right-rail">
            <view class="author-rail" @tap.stop="openAuthor(item.author.id)">
              <image class="rail-avatar" :src="item.author.avatar" mode="aspectFill" />
              <view class="follow-pill">关注</view>
            </view>

            <view class="rail-action" @tap.stop="toggleLike(item)">
              <view class="rail-icon-circle">
                <text class="rail-icon">{{ item.isLiked ? '♥' : '♡' }}</text>
              </view>
              <text class="rail-text">{{ item.likeCount }}</text>
            </view>

            <view class="rail-action" @tap.stop="toggleFavorite(item)">
              <view class="rail-icon-circle">
                <text class="rail-icon">{{ item.isFavorited ? '★' : '☆' }}</text>
              </view>
              <text class="rail-text">收藏</text>
            </view>

            <view class="rail-action" @tap.stop="shareItem(item)">
              <view class="rail-icon-circle">
                <text class="rail-icon">⇪</text>
              </view>
              <text class="rail-text">分享</text>
            </view>
          </view>

          <view class="vlog-body">
            <view class="location-chip">
              <text class="chip-icon">◎</text>
              <text class="chip-text">{{ item.location }}</text>
            </view>
            <text class="author-handle">@{{ item.author.nickname }}</text>
            <text class="vlog-title">{{ item.title }}</text>
            <text class="vlog-desc">{{ item.content }}</text>
            <view class="detail-pill" @tap="openDetail(item.id)">进入详情与评论</view>
          </view>
        </view>
      </swiper-item>
    </swiper>
    <FloatingPublishButton />
  </view>
</template>

<script>
import { getPostList } from '../../api/modules/post'
import { sharePost, togglePostFavorite, togglePostLike } from '../../api/modules/post'
import { go } from '../../utils/navigation'
import FloatingPublishButton from '../../components/common/FloatingPublishButton.vue'

export default {
  components: {
    FloatingPublishButton
  },
  data() {
    return {
      list: []
    }
  },
  onLoad() {
    this.fetchList()
  },
  methods: {
    async fetchList() {
      const result = await getPostList()
      this.list = result.list
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
  min-height: 100vh;
  position: relative;
  background: #0a0d12;
}

.search-float {
  position: fixed;
  top: 92rpx;
  left: 48rpx;
  right: 48rpx;
  z-index: 5;
  height: 92rpx;
  border-radius: 999rpx;
  padding: 0 30rpx;
  display: flex;
  align-items: center;
  background: rgba(39, 44, 51, 0.58);
  border: 2rpx solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(18rpx);
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

.vlog-swiper {
  height: 100vh;
}

.vlog-item {
  position: relative;
  height: 100vh;
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
    linear-gradient(180deg, rgba(0, 0, 0, 0.12) 0%, rgba(0, 0, 0, 0.18) 18%, rgba(0, 0, 0, 0.18) 42%, rgba(0, 0, 0, 0.62) 88%, rgba(0, 0, 0, 0.86) 100%);
}

.top-fade {
  position: absolute;
  inset: 0 0 auto 0;
  height: 320rpx;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.28) 0%, rgba(0, 0, 0, 0) 100%);
  z-index: 1;
}

.right-rail {
  position: absolute;
  right: 24rpx;
  bottom: 310rpx;
  z-index: 3;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 28rpx;
}

.author-rail {
  position: relative;
  width: 96rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.rail-avatar {
  width: 88rpx;
  height: 88rpx;
  border-radius: 50%;
  border: 4rpx solid rgba(255, 255, 255, 0.45);
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

.rail-text {
  margin-top: 12rpx;
  font-size: 24rpx;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.92);
}

.vlog-body {
  position: absolute;
  left: 34rpx;
  right: 146rpx;
  bottom: 220rpx;
  z-index: 3;
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
  color: rgba(255, 255, 255, 0.9);
  letter-spacing: 1rpx;
}

.author-handle {
  margin-top: 28rpx;
  font-size: 28rpx;
  font-weight: 700;
  color: #ffffff;
}

.vlog-title {
  margin-top: 14rpx;
  font-size: 56rpx;
  line-height: 1.12;
  font-weight: 700;
  color: #ffffff;
}

.vlog-desc {
  margin-top: 18rpx;
  width: 100%;
  font-size: 26rpx;
  line-height: 1.65;
  color: rgba(255, 255, 255, 0.72);
}

.detail-pill {
  margin-top: 24rpx;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 220rpx;
  height: 68rpx;
  padding: 0 26rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.16);
  color: #ffffff;
  font-size: 22rpx;
  font-weight: 600;
}
</style>
