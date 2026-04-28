<template>
  <view v-if="profile" class="page-shell">
    <AppHeader title="作者主页" subtitle="Public Profile" fallback="/pages/home/index" />
    <view class="hero glass-card">
      <image class="avatar" :src="profile.avatar" mode="aspectFill" />
      <text class="name">{{ profile.nickname }}</text>
      <text class="bio">{{ profile.bio }}</text>
    </view>
    <view class="two-column-grid">
      <view v-for="item in profile.posts" :key="item.id" class="content-card profile-card" @tap="openContent(item)">
        <video
          v-if="item.type === 'vlog' && hasVideo(item)"
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
        <image v-else class="profile-card-image" :src="item.coverUrl" mode="aspectFill" />
        <view class="profile-card-body">
          <text class="profile-card-title">{{ item.title }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import AppHeader from '../../components/common/AppHeader.vue'
import { getUserPublicProfile } from '../../api/modules/user'
import { getPostPosterUrl, getPostVideoUrl, hasPostVideo } from '../../utils/post-media'
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
    this.profile = await getUserPublicProfile(options && options.userId)
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
    openContent(item) {
      if (item.type === 'vlog') {
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

.two-column-grid {
  margin-top: 24rpx;
}

.profile-card {
  overflow: hidden;
}

.profile-card-image {
  width: 100%;
  height: 260rpx;
}

.profile-card-body {
  padding: 18rpx;
}

.profile-card-title {
  font-size: 24rpx;
  line-height: 1.5;
}
</style>
