<script setup>
import { reactive } from "vue";
import { onShow } from "@dcloudio/uni-app";

import AppNavBar from "@/components/AppNavBar.vue";
import { ROUTES } from "@/constants/routes";
import { resolveAssetUrl, uploadImage } from "@/api/request";
import { ensureLoggedIn, useAuthGuard } from "@/composables/useAuthGuard";
import { useProfileStore } from "@/stores/profile";
import { go } from "@/utils/navigation";

useAuthGuard();

const profileStore = useProfileStore();
const genderOptions = ["unknown", "male", "female"];
const form = reactive({
  nickname: "",
  bio: "",
  avatar: "",
  gender: "unknown",
});

onShow(async () => {
  if (!ensureLoggedIn()) {
    return;
  }
  try {
    const profile = await profileStore.fetchProfile();
    form.nickname = profile.nickname;
    form.bio = profile.bio;
    form.avatar = profile.avatar;
    form.gender = profile.gender;
  } catch (error) {
    uni.showToast({
      title: error instanceof Error ? error.message : "加载失败",
      icon: "none",
    });
  }
});

async function chooseAvatar() {
  try {
    const filePath = await new Promise((resolve, reject) => {
      uni.chooseImage({
        count: 1,
        success: (result) => resolve(result.tempFilePaths[0]),
        fail: reject,
      });
    });
    const uploadResult = await uploadImage(filePath);
    form.avatar = uploadResult.url;
  } catch (error) {
    uni.showToast({
      title: error instanceof Error ? error.message : "上传失败",
      icon: "none",
    });
  }
}

async function saveProfile() {
  try {
    await profileStore.saveProfile(form);
    uni.showToast({ title: "已保存", icon: "success" });
  } catch (error) {
    uni.showToast({
      title: error instanceof Error ? error.message : "保存失败",
      icon: "none",
    });
  }
}

function onGenderChange(event) {
  const nextGender = genderOptions[event.detail.value] || "unknown";
  form.gender = nextGender;
}
</script>

<template>
  <view class="page-shell">
    <AppNavBar title="个人资料" subtitle="Profile" />

    <view class="card-stack">
      <view class="glass-card panel">
        <text class="section-kicker">Avatar</text>
        <view class="avatar-row">
          <image v-if="form.avatar" class="avatar-image" :src="resolveAssetUrl(form.avatar)" mode="aspectFill" />
          <view v-else class="avatar-fallback">{{ form.nickname.slice(0, 1) || "F" }}</view>
          <button class="secondary-button avatar-button" @tap="chooseAvatar">上传头像</button>
        </view>
      </view>

      <view class="glass-card panel">
        <view class="field-block">
          <text class="label-text">昵称</text>
          <input v-model="form.nickname" class="field-input" />
        </view>
        <view class="field-block">
          <text class="label-text">简介</text>
          <textarea v-model="form.bio" class="field-textarea" maxlength="300" />
        </view>
        <view class="field-block">
          <text class="label-text">性别</text>
          <picker :range="genderOptions" @change="onGenderChange">
            <view class="field-picker">{{ form.gender }}</view>
          </picker>
        </view>
        <button class="primary-button action-button" @tap="saveProfile">保存资料</button>
      </view>

      <view class="glass-card panel">
        <button class="secondary-button action-button" @tap="go(ROUTES.settings)">进入设置</button>
      </view>
    </view>
  </view>
</template>

<style scoped lang="scss">
.panel {
  border-radius: 34rpx;
  padding: 30rpx;
}

.avatar-row {
  display: flex;
  align-items: center;
  gap: 22rpx;
  margin-top: 20rpx;
}

.avatar-image,
.avatar-fallback {
  width: 132rpx;
  height: 132rpx;
  border-radius: 999rpx;
}

.avatar-fallback {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(236, 214, 179, 0.2);
  font-size: 44rpx;
  font-weight: 700;
}

.avatar-button,
.action-button {
  margin-top: 24rpx;
}

.field-block {
  margin-top: 20rpx;
}
</style>
