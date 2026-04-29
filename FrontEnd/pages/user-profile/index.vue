<template>
  <view v-if="profile" class="page-shell">
    <AppHeader title="作者主页" subtitle="Public Profile" fallback="/pages/home/index" />
    <view class="hero glass-card">
      <image class="avatar" :src="profile.avatar" mode="aspectFill" />
      <text class="name">{{ profile.nickname }}</text>
      <text class="bio">{{ profile.bio }}</text>
    </view>
    <view class="stats-row glass-card">
      <view class="stat-item">
        <text class="stat-number">{{ profile.stats.posts }}</text>
        <text class="stat-label">发布</text>
      </view>
      <view class="stat-item">
        <text class="stat-number">{{ profile.stats.favorites }}</text>
        <text class="stat-label">获收藏</text>
      </view>
      <view class="stat-item">
        <text class="stat-number">{{ profile.stats.likes }}</text>
        <text class="stat-label">获点赞</text>
      </view>
    </view>
    <view class="section-head">
      <text class="section-title">TA 的发布</text>
      <text class="section-subtitle">{{ profile.posts.length }} 条内容</text>
    </view>
    <view class="two-column-grid">
      <view v-for="item in profile.posts" :key="item.id" class="content-card profile-card" @tap="openContent(item)">
        <video
          v-if="isVlog(item) && hasVideo(item)"
          class="profile-card-image"
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
        <image v-else-if="getCardCover(item)" class="profile-card-image" :src="getCardCover(item)" mode="aspectFill" />
        <view v-else class="profile-card-image profile-card-fallback">
          <text class="fallback-tag">{{ isVlog(item) ? 'VLOG' : '攻略' }}</text>
          <text class="fallback-text">{{ item.title || '查看内容详情' }}</text>
        </view>
        <view class="profile-card-body">
          <text class="profile-card-title">{{ item.title }}</text>
          <text class="profile-card-meta">{{ isVlog(item) ? 'Vlog' : '攻略' }}</text>
        </view>
      </view>
    </view>
    <view v-if="!profile.posts.length" class="empty-card glass-card">
      <text class="empty-title">还没有公开发布内容</text>
      <text class="empty-desc">等 TA 发布攻略或 Vlog 后，这里就会显示。</text>
    </view>
  </view>
</template>

<script>
import AppHeader from '../../components/common/AppHeader.vue'
import { getUserPublicProfile, getUserPublishedContent } from '../../api/modules/user'
import { getPostPosterUrl, getPostVideoUrl, hasPostVideo, isVideoLikeUrl } from '../../utils/post-media'
import { go } from '../../utils/navigation'

export default {
  components: {
    AppHeader
  },
  data() {
    return {
      profile: null
    }
  },
  async onLoad(options) {
    const userId = options && options.userId
    const [profile, contents] = await Promise.all([
      getUserPublicProfile(userId),
      getUserPublishedContent(userId)
    ])
    this.profile = {
      ...profile,
      stats: {
        posts: profile.stats && profile.stats.posts ? profile.stats.posts : 0,
        favorites: profile.stats && profile.stats.favorites ? profile.stats.favorites : 0,
        likes: profile.stats && profile.stats.likes ? profile.stats.likes : 0
      },
      posts: Array.isArray(contents.list) ? contents.list : []
    }
  },
  methods: {
    isVlog(item) {
      return item && (item.type === 'vlog' || item.contentType === 'vlog')
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
    getCardCover(item) {
      if (!item) {
        return ''
      }
      if (this.isVlog(item)) {
        const posterUrl = this.getPosterUrl(item)
        if (posterUrl) {
          return posterUrl
        }
      }
      if (item.coverUrl && !isVideoLikeUrl(item.coverUrl)) {
        return item.coverUrl
      }
      if (Array.isArray(item.imageList) && item.imageList.length) {
        const firstImage = item.imageList[0]
        return typeof firstImage === 'string' ? firstImage : firstImage && firstImage.url ? firstImage.url : ''
      }
      return ''
    },
    openContent(item) {
      if (this.isVlog(item)) {
        go(`/pages/vlog-detail/index?id=${item.id}`)
        return
      }
      go(`/pages/strategy-detail/index?id=${item.id}`)
    }
  }
}
</script>

<style scoped lang="scss">
.hero {
  padding: 34rpx;
  border-radius: 32rpx;
  text-align: center;
}

.avatar {
  width: 130rpx;
  height: 130rpx;
  border-radius: 50%;
}

.name {
  display: block;
  margin-top: 18rpx;
  font-size: 40rpx;
  font-weight: 700;
}

.bio {
  display: block;
  margin-top: 12rpx;
  font-size: 24rpx;
  color: rgba(246, 240, 232, 0.68);
  line-height: 1.7;
}

.stats-row {
  margin-top: 24rpx;
  padding: 24rpx 28rpx;
  border-radius: 28rpx;
  display: flex;
  justify-content: space-between;
}

.stat-item {
  flex: 1;
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 36rpx;
  font-weight: 700;
}

.stat-label {
  display: block;
  margin-top: 10rpx;
  font-size: 22rpx;
  color: rgba(246, 240, 232, 0.56);
}

.section-head {
  margin-top: 28rpx;
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}

.section-title {
  font-size: 30rpx;
  font-weight: 700;
}

.section-subtitle {
  font-size: 22rpx;
  color: rgba(246, 240, 232, 0.54);
}

.two-column-grid {
  margin-top: 24rpx;
}

.profile-card {
  overflow: hidden;
}

.profile-card-image,
.profile-card-fallback {
  width: 100%;
  height: 260rpx;
}

.profile-card-fallback {
  padding: 24rpx;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  background:
    linear-gradient(180deg, rgba(10, 13, 18, 0.12) 0%, rgba(10, 13, 18, 0.82) 100%),
    linear-gradient(145deg, #17314a 0%, #102033 55%, #0a111a 100%);
}

.fallback-tag {
  font-size: 20rpx;
  letter-spacing: 4rpx;
  color: rgba(246, 240, 232, 0.56);
}

.fallback-text {
  margin-top: 14rpx;
  font-size: 26rpx;
  line-height: 1.4;
  font-weight: 700;
}

.profile-card-body {
  padding: 18rpx;
}

.profile-card-title {
  font-size: 24rpx;
  line-height: 1.5;
}

.profile-card-meta {
  display: block;
  margin-top: 10rpx;
  font-size: 22rpx;
  color: rgba(246, 240, 232, 0.5);
}

.empty-card {
  margin-top: 24rpx;
  padding: 34rpx 28rpx;
  border-radius: 28rpx;
  text-align: center;
}

.empty-title {
  display: block;
  font-size: 28rpx;
  font-weight: 700;
}

.empty-desc {
  display: block;
  margin-top: 12rpx;
  font-size: 22rpx;
  line-height: 1.7;
  color: rgba(246, 240, 232, 0.56);
}
</style>
