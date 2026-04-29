<template>
  <view class="page-shell login-page">
    <image class="bg-image" src="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&q=80&w=2000" mode="aspectFill" />
    <view class="bg-mask" />
    <view class="login-content">
      <view>
        <text class="brand">远方</text>
        <text class="tagline">把下一个目的地，变成你可以立刻出发的故事。</text>
      </view>

      <view class="login-actions glass-card">
        <template v-if="viewMode === 'entry'">
          <text class="panel-title">选择登录方式</text>
          <button class="ghost-btn action-btn" @tap="openAccountAuth">账号密码登录 / 注册</button>
          <button class="ghost-btn action-btn" @tap="showTip('手机号登录暂未开放')">手机号登录</button>
          <button class="wechat-btn action-btn" @tap="showTip('微信授权登录暂未开放')">微信授权登录</button>
        </template>

        <template v-else>
          <view class="form-head">
            <view class="back-link" @tap="backToEntry">‹ 返回</view>
            <view class="auth-tabs">
              <view class="auth-tab" :class="{ active: authMode === 'login' }" @tap="switchAuthMode('login')">登录</view>
              <view class="auth-tab" :class="{ active: authMode === 'register' }" @tap="switchAuthMode('register')">注册</view>
            </view>
          </view>

          <view v-if="authMode === 'register'" class="field-card">
            <text class="field-label">昵称</text>
            <input v-model.trim="form.nickname" class="field-input" placeholder="输入昵称，可选" placeholder-style="color: rgba(12,19,32,0.36)" />
          </view>
          <view class="field-card">
            <text class="field-label">账号</text>
            <input v-model.trim="form.username" class="field-input" placeholder="输入用户名" placeholder-style="color: rgba(12,19,32,0.36)" />
          </view>
          <text v-if="authMode === 'register'" class="field-tip">用户名限 3-32 位，只能使用字母、数字和下划线</text>
          <view class="field-card">
            <text class="field-label">密码</text>
            <input v-model="form.password" class="field-input" password placeholder="输入密码" placeholder-style="color: rgba(12,19,32,0.36)" />
          </view>
          <text v-if="authMode === 'register'" class="field-tip">密码需为 6-128 位</text>
          <view v-if="authMode === 'register'" class="field-card">
            <text class="field-label">确认密码</text>
            <input v-model="form.confirmPassword" class="field-input" password placeholder="再次输入密码" placeholder-style="color: rgba(12,19,32,0.36)" />
          </view>

          <button class="primary-button action-btn" @tap="submitAccountAuth">
            {{ authMode === 'login' ? '账号密码登录' : '立即注册' }}
          </button>
          <text class="form-hint">
            {{ authMode === 'login' ? '使用已注册账号登录 Faraway。' : '注册成功后将自动为你登录。' }}
          </text>
        </template>
      </view>

      <text class="agreement">继续操作即代表你同意《服务协议》与《隐私政策》</text>
    </view>
  </view>
</template>

<script>
import { passwordLogin, registerByPassword } from '../../api/modules/auth'
import { useUserStore } from '../../stores/user'
import { isLoggedIn } from '../../utils/auth'

const USERNAME_PATTERN = /^[A-Za-z0-9_]+$/

export default {
  data() {
    return {
      viewMode: 'entry',
      authMode: 'login',
      form: {
        nickname: '',
        username: '',
        password: '',
        confirmPassword: ''
      }
    }
  },
  onShow() {
    this.redirectIfLoggedIn()
  },
  methods: {
    redirectIfLoggedIn() {
      if (!isLoggedIn()) {
        return
      }
      uni.switchTab({
        url: '/pages/home/index'
      })
    },
    completeLogin(result) {
      const token = result && typeof result.token === 'string' ? result.token : ''
      const userInfo = result && result.userInfo && typeof result.userInfo === 'object' ? result.userInfo : null
      if (!token || !userInfo) {
        throw new Error('登录响应格式不正确')
      }
      const userStore = useUserStore()
      userStore.login(token, userInfo)
      uni.switchTab({
        url: '/pages/home/index'
      })
    },
    openAccountAuth() {
      this.viewMode = 'account'
    },
    backToEntry() {
      this.viewMode = 'entry'
    },
    switchAuthMode(mode) {
      this.authMode = mode
      this.form.password = ''
      this.form.confirmPassword = ''
    },
    async handlePasswordLogin() {
      if (!this.form.username || !this.form.password) {
        uni.showToast({
          title: '请输入账号和密码',
          icon: 'none'
        })
        return
      }

      try {
        const result = await passwordLogin(this.form)
        this.completeLogin(result)
      } catch (error) {
        uni.showToast({
          title: error && error.message ? error.message : '登录失败',
          icon: 'none'
        })
      }
    },
    async handleRegister() {
      if (!this.form.username || !this.form.password || !this.form.confirmPassword) {
        uni.showToast({
          title: '请填写完整注册信息',
          icon: 'none'
        })
        return
      }
      if (this.form.username.length < 3 || this.form.username.length > 32) {
        uni.showToast({
          title: '用户名需为 3-32 位',
          icon: 'none'
        })
        return
      }
      if (!USERNAME_PATTERN.test(this.form.username)) {
        uni.showToast({
          title: '用户名仅支持字母数字下划线',
          icon: 'none'
        })
        return
      }
      if (this.form.password.length < 6 || this.form.password.length > 128) {
        uni.showToast({
          title: '密码需为 6-128 位',
          icon: 'none'
        })
        return
      }
      if (this.form.password !== this.form.confirmPassword) {
        uni.showToast({
          title: '两次输入的密码不一致',
          icon: 'none'
        })
        return
      }
      try {
        await registerByPassword(this.form)
        const result = await passwordLogin(this.form)
        this.completeLogin(result)
      } catch (error) {
        uni.showToast({
          title: error && error.message ? error.message : '注册失败',
          icon: 'none'
        })
      }
    },
    submitAccountAuth() {
      if (this.authMode === 'login') {
        this.handlePasswordLogin()
        return
      }
      this.handleRegister()
    },
    showTip(message) {
      uni.showToast({
        title: message,
        icon: 'none'
      })
    }
  }
}
</script>

<style scoped lang="scss">
.login-page {
  overflow: hidden;
}

.bg-image,
.bg-mask {
  position: fixed;
  inset: 0;
}

.bg-image {
  width: 100%;
  height: 100%;
}

.bg-mask {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.14) 0%, rgba(7, 17, 31, 0.1) 40%, rgba(7, 17, 31, 0.84) 100%);
}

.login-content {
  position: relative;
  z-index: 2;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 120rpx 10rpx 60rpx;
}

.brand {
  display: block;
  font-size: 120rpx;
  font-style: italic;
  font-weight: 700;
  color: #101213;
}

.tagline {
  display: block;
  margin-top: 24rpx;
  width: 72%;
  font-size: 28rpx;
  line-height: 1.8;
  color: rgba(16, 18, 19, 0.72);
}

.login-actions {
  padding: 26rpx;
  border-radius: 36rpx;
}

.panel-title {
  display: block;
  margin-bottom: 8rpx;
  font-size: 30rpx;
  font-weight: 700;
  color: #0c1320;
}

.form-head {
  display: flex;
  flex-direction: column;
  gap: 18rpx;
}

.back-link {
  font-size: 24rpx;
  color: rgba(12, 19, 32, 0.68);
}

.auth-tabs {
  display: flex;
  gap: 16rpx;
}

.auth-tab {
  flex: 1;
  height: 76rpx;
  border-radius: 999rpx;
  background: rgba(12, 19, 32, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26rpx;
  font-weight: 700;
  color: rgba(12, 19, 32, 0.56);
}

.auth-tab.active {
  background: #0c1320;
  color: #ffffff;
}

.field-card {
  margin-top: 18rpx;
  padding: 24rpx 26rpx;
  border-radius: 28rpx;
  background: rgba(255, 255, 255, 0.86);
}

.field-label {
  display: block;
  font-size: 22rpx;
  color: rgba(12, 19, 32, 0.52);
  letter-spacing: 4rpx;
}

.field-input {
  margin-top: 12rpx;
  font-size: 28rpx;
  color: #0c1320;
}

.field-tip {
  display: block;
  margin-top: 10rpx;
  margin-left: 12rpx;
  font-size: 22rpx;
  color: rgba(12, 19, 32, 0.52);
}

.action-btn {
  width: 100%;
  margin-top: 18rpx;
}

.ghost-btn,
.wechat-btn {
  height: 92rpx;
  border-radius: 999rpx;
  font-size: 28rpx;
  font-weight: 700;
}

.ghost-btn {
  background: rgba(255, 255, 255, 0.82);
  color: #0c1320;
}

.wechat-btn {
  background: #07c160;
  color: #ffffff;
}

.form-hint {
  display: block;
  margin-top: 18rpx;
  text-align: center;
  font-size: 22rpx;
  color: rgba(12, 19, 32, 0.56);
}

.agreement {
  display: block;
  margin-top: 32rpx;
  text-align: center;
  font-size: 22rpx;
  color: rgba(246, 240, 232, 0.52);
}
</style>
