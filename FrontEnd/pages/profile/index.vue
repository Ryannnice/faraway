<template>
  <view class="page-shell with-safe-bottom">
    <image class="profile-cover" :src="user.avatar" mode="aspectFill" />
    <view class="profile-mask" />
    <view class="profile-content">
      <view class="profile-top">
        <image class="profile-avatar" :src="user.avatar" mode="aspectFill" />
        <view class="profile-meta">
          <text class="profile-name">{{ user.nickname }}</text>
          <text class="profile-bio">{{ user.bio }}</text>
        </view>
      </view>

      <view class="stats-row glass-card">
        <view class="stat-item">
          <text class="stat-number">{{ user.stats.posts }}</text>
          <text class="stat-label">发布</text>
        </view>
        <view class="stat-item">
          <text class="stat-number">{{ user.stats.favorites }}</text>
          <text class="stat-label">收藏</text>
        </view>
        <view class="stat-item">
          <text class="stat-number">{{ user.stats.likes }}</text>
          <text class="stat-label">点赞</text>
        </view>
      </view>

      <view class="menu-grid">
        <view class="menu-card glass-card" @tap="goPage('/pages/my-posts/index')">我的发布</view>
        <view class="menu-card glass-card" @tap="goPage('/pages/drafts/index')">草稿箱</view>
        <view class="menu-card glass-card" @tap="goPage('/pages/my-favorites/index')">我的收藏</view>
        <view class="menu-card glass-card" @tap="goPage('/pages/my-likes/index')">我的点赞</view>
        <view class="menu-card glass-card" @tap="goPage('/pages/my-partners/index')">我的搭子</view>
        <view class="menu-card glass-card" @tap="goPage('/pages/settings/index')">设置</view>
      </view>
    </view>
    <FloatingPublishButton />
  </view>
</template>

<script>
import { getMyStats, getUserProfile } from '../../api/modules/user'
import FloatingPublishButton from '../../components/common/FloatingPublishButton.vue'
import { useUserStore } from '../../stores/user'
import { go } from '../../utils/navigation'

export default {
  components: {
    FloatingPublishButton
  },
  data() {
    return {
      user: {
        avatar: '',
        nickname: '',
        bio: '',
        stats: {
          posts: 0,
          favorites: 0,
          likes: 0
        }
      }
    }
  },
  onShow() {
    this.loadProfile()
  },
  methods: {
    async loadProfile() {
      const userStore = useUserStore()
      const [profile, stats] = await Promise.all([
        getUserProfile(),
        getMyStats()
      ])
      const nextUser = {
        ...userStore.userInfo,
        ...profile,
        stats: {
          posts: (stats.postCount || 0) + (stats.strategyCount || 0),
          favorites: stats.favoriteCount || 0,
          likes: stats.likeCount || 0
        }
      }
      this.user = nextUser
      userStore.setProfile(nextUser)
    },
    goPage(url) {
      go(url)
    }
  }
}
</script>

<style scoped lang="scss">
.profile-cover,
.profile-mask {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  height: 420rpx;
}

.profile-cover {
  width: 100%;
}

.profile-mask {
  background: linear-gradient(180deg, rgba(7, 17, 31, 0.18) 0%, rgba(7, 17, 31, 0.82) 100%);
}

.profile-content {
  position: relative;
  z-index: 2;
  margin-top: 220rpx;
}

.profile-top {
  display: flex;
  align-items: flex-end;
}

.profile-avatar {
  width: 156rpx;
  height: 156rpx;
  border-radius: 42rpx;
  border: 4rpx solid rgba(255, 255, 255, 0.18);
}

.profile-meta {
  margin-left: 24rpx;
}

.profile-name {
  display: block;
  font-size: 52rpx;
  font-weight: 700;
}

.profile-bio {
  display: block;
  margin-top: 12rpx;
  font-size: 24rpx;
  line-height: 1.7;
  color: rgba(246, 240, 232, 0.68);
}

.stats-row {
  margin-top: 28rpx;
  padding: 28rpx;
  border-radius: 32rpx;
  display: flex;
  justify-content: space-between;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 38rpx;
  font-weight: 700;
}

.stat-label {
  display: block;
  margin-top: 10rpx;
  font-size: 22rpx;
  color: rgba(246, 240, 232, 0.5);
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18rpx;
  margin-top: 24rpx;
}

.menu-card {
  padding: 34rpx 28rpx;
  border-radius: 30rpx;
  text-align: center;
  font-size: 28rpx;
  color: #f6f0e8;
}
</style>
