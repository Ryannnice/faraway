<template>
  <view class="page-shell">
    <AppHeader title="系统设置" subtitle="Settings" fallback="/pages/profile/index" />
    <view class="field glass-card">
      <text class="field-label">昵称</text>
      <input v-model="form.nickname" class="field-input" />
    </view>
    <view class="field glass-card">
      <text class="field-label">简介</text>
      <textarea v-model="form.bio" class="field-textarea" />
    </view>
    <button class="primary-button save-btn" @tap="saveProfile">保存资料</button>
    <button class="logout-btn" @tap="logout">退出登录</button>
  </view>
</template>

<script>
import AppHeader from '../../components/common/AppHeader.vue'
import { getUserProfile, updateUserProfile } from '../../api/modules/user'
import { useUserStore } from '../../stores/user'

export default {
  components: {
    AppHeader
  },
  data() {
    return {
      form: {
        nickname: '',
        bio: ''
      }
    }
  },
  onShow() {
    this.loadProfile()
  },
  methods: {
    async loadProfile() {
      const profile = await getUserProfile()
      this.form.nickname = profile.nickname || ''
      this.form.bio = profile.bio || ''
    },
    async saveProfile() {
      const userStore = useUserStore()
      const updated = await updateUserProfile(this.form)
      userStore.setProfile({
        ...userStore.userInfo,
        ...updated
      })
      uni.showToast({
        title: '已保存',
        icon: 'none'
      })
    },
    logout() {
      const userStore = useUserStore()
      userStore.logout()
      uni.reLaunch({
        url: '/pages/login/index'
      })
    }
  }
}
</script>

<style scoped lang="scss">
.field {
  margin-top: 24rpx;
  padding: 28rpx;
  border-radius: 30rpx;
}

.field-label {
  display: block;
  font-size: 22rpx;
  letter-spacing: 4rpx;
  color: rgba(246, 240, 232, 0.46);
}

.field-input,
.field-textarea {
  margin-top: 16rpx;
  color: #f6f0e8;
  font-size: 30rpx;
}

.field-textarea {
  min-height: 200rpx;
  width: 100%;
}

.save-btn {
  margin-top: 28rpx;
}

.logout-btn {
  margin-top: 18rpx;
  height: 92rpx;
  border-radius: 999rpx;
  background: rgba(255, 141, 122, 0.14);
  color: #ff8d7a;
  font-size: 28rpx;
  font-weight: 700;
}
</style>
