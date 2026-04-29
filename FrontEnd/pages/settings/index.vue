<template>
  <view class="page-shell">
    <AppHeader title="系统设置" subtitle="Settings" fallback="/pages/profile/index" />
    <view class="field glass-card">
      <text class="field-label">头像</text>
      <view class="avatar-panel">
        <image class="avatar-preview" :src="form.avatar || defaultAvatar" mode="aspectFill" />
        <view class="avatar-actions">
          <button class="ghost-button avatar-btn" @tap="chooseAvatar">更换头像</button>
          <button class="ghost-button avatar-btn" @tap="useDefaultAvatar">使用默认头像</button>
        </view>
      </view>
      <view class="preset-grid">
        <image
          v-for="item in presetAvatars"
          :key="item"
          class="preset-avatar"
          :class="{ active: form.avatar === item }"
          :src="item"
          mode="aspectFill"
          @tap="selectPreset(item)"
        />
      </view>
    </view>
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
import { uploadImage } from '../../api/modules/upload'
import { getUserProfile, updateUserProfile } from '../../api/modules/user'
import { useUserStore } from '../../stores/user'

const DEFAULT_AVATAR = 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=400'
const PRESET_AVATARS = [
  DEFAULT_AVATAR,
  'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&q=80&w=400',
  'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&q=80&w=400',
  'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&q=80&w=400'
]

export default {
  components: {
    AppHeader
  },
  data() {
    return {
      defaultAvatar: DEFAULT_AVATAR,
      presetAvatars: PRESET_AVATARS,
      form: {
        avatar: '',
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
      this.form.avatar = profile.avatar || ''
      this.form.nickname = profile.nickname || ''
      this.form.bio = profile.bio || ''
    },
    async chooseAvatar() {
      try {
        const result = await new Promise((resolve, reject) => {
          uni.chooseImage({
            count: 1,
            sizeType: ['compressed'],
            sourceType: ['album', 'camera'],
            success: resolve,
            fail: reject
          })
        })
        const file = result && result.tempFiles && result.tempFiles[0]
        if (!file) {
          return
        }
        uni.showLoading({
          title: '上传中'
        })
        const uploaded = await uploadImage(file)
        this.form.avatar = uploaded.url || this.form.avatar
      } catch (error) {
        if (error && error.errMsg && error.errMsg.includes('cancel')) {
          return
        }
        uni.showToast({
          title: '头像上传失败',
          icon: 'none'
        })
      } finally {
        uni.hideLoading()
      }
    },
    useDefaultAvatar() {
      this.form.avatar = this.defaultAvatar
    },
    selectPreset(url) {
      this.form.avatar = url
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

.avatar-panel {
  margin-top: 18rpx;
  display: flex;
  align-items: center;
}

.avatar-preview {
  width: 132rpx;
  height: 132rpx;
  border-radius: 36rpx;
  background: rgba(255, 255, 255, 0.08);
}

.avatar-actions {
  flex: 1;
  margin-left: 22rpx;
  display: flex;
  flex-direction: column;
  gap: 14rpx;
}

.avatar-btn {
  width: 100%;
  height: 78rpx;
  border-radius: 999rpx;
  font-size: 24rpx;
}

.ghost-button {
  background: rgba(255, 255, 255, 0.12);
  color: #f6f0e8;
}

.preset-grid {
  margin-top: 20rpx;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16rpx;
}

.preset-avatar {
  width: 100%;
  height: 120rpx;
  border-radius: 28rpx;
  border: 4rpx solid transparent;
}

.preset-avatar.active {
  border-color: #ecd6b3;
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
