<script setup>
import { reactive, ref } from "vue";

import { publishVlog } from "@/api/content";
import { resolveAssetUrl, uploadImage } from "@/api/request";
import AppNavBar from "@/components/AppNavBar.vue";
import { ROUTES } from "@/constants/routes";
import { useAuthGuard } from "@/composables/useAuthGuard";
import { go } from "@/utils/navigation";

useAuthGuard();

const form = reactive({
  title: "",
  content: "",
  tagsText: "",
  images: [],
});
const publishing = ref(false);
const uploading = ref(false);

function normalizeTags(text) {
  const parts = text.split(/[\n,，、 ]+/);
  const seen = {};
  const next = [];
  parts.forEach((item) => {
    const value = item.trim();
    if (!value || seen[value]) {
      return;
    }
    seen[value] = true;
    next.push(value);
  });
  return next.slice(0, 5);
}

async function chooseImages() {
  if (uploading.value || form.images.length >= 9) {
    return;
  }
  uploading.value = true;
  try {
    const picked = await new Promise((resolve, reject) => {
      uni.chooseImage({
        count: 9 - form.images.length,
        success: resolve,
        fail: reject,
      });
    });
    const nextFiles = picked.tempFilePaths || [];
    for (const filePath of nextFiles) {
      const uploaded = await uploadImage(filePath);
      form.images.push(uploaded);
    }
  } catch (error) {
    uni.showToast({
      title: error instanceof Error ? error.message : "上传失败",
      icon: "none",
    });
  } finally {
    uploading.value = false;
  }
}

function removeImage(index) {
  form.images.splice(index, 1);
}

function confirmPublish() {
  if (publishing.value) {
    return;
  }
  uni.showModal({
    title: "确认发布",
    content: "发布后当前阶段不能编辑和删除，确认继续吗？",
    success: async (modalResult) => {
      if (!modalResult.confirm) {
        return;
      }
      publishing.value = true;
      try {
        const published = await publishVlog({
          title: form.title,
          content: form.content,
          tags: normalizeTags(form.tagsText),
          image_asset_ids: form.images.map((item) => item.asset_id),
        });
        uni.showToast({ title: "发布成功", icon: "success" });
        go(`${ROUTES.contentDetail}?content_id=${published.content_id}`);
      } catch (error) {
        uni.showToast({
          title: error instanceof Error ? error.message : "发布失败",
          icon: "none",
        });
      } finally {
        publishing.value = false;
      }
    },
  });
}
</script>

<template>
  <view class="page-shell">
    <AppNavBar title="发图文" subtitle="Graphic Post" />

    <view class="glass-card panel">
      <view class="field-block">
        <text class="label-text">标题</text>
        <input v-model="form.title" class="field-input" maxlength="60" placeholder="给这篇图文起个名字" />
      </view>

      <view class="field-block">
        <text class="label-text">正文</text>
        <textarea v-model="form.content" class="field-textarea" maxlength="5000" placeholder="记录这次旅行的片段、感受和路线。" />
      </view>

      <view class="field-block">
        <text class="label-text">业务标签</text>
        <input v-model="form.tagsText" class="field-input" placeholder="例如：夜景, 咖啡店, 旧城散步" />
      </view>

      <view class="field-block">
        <text class="label-text">图片</text>
        <view class="image-grid">
          <view v-for="(item, index) in form.images" :key="item.asset_id" class="image-card">
            <image class="image-preview" :src="resolveAssetUrl(item.url)" mode="aspectFill" />
            <view class="image-remove" @tap="removeImage(index)">移除</view>
          </view>
          <view v-if="form.images.length < 9" class="image-picker" @tap="chooseImages">
            {{ uploading ? "上传中..." : "上传图片" }}
          </view>
        </view>
      </view>

      <button class="primary-button submit-button" :class="{ 'button-disabled': publishing }" @tap="confirmPublish">
        {{ publishing ? "发布中..." : "发布图文" }}
      </button>
    </view>
  </view>
</template>

<style scoped lang="scss">
.panel {
  border-radius: 34rpx;
  padding: 30rpx;
}

.field-block {
  margin-top: 20rpx;
}

.submit-button {
  margin-top: 30rpx;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16rpx;
}

.image-card,
.image-picker {
  position: relative;
  width: 100%;
  height: 240rpx;
  border-radius: 24rpx;
  overflow: hidden;
}

.image-preview {
  width: 100%;
  height: 100%;
}

.image-picker {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border: 1rpx dashed rgba(255, 255, 255, 0.16);
  color: rgba(246, 240, 232, 0.72);
}

.image-remove {
  position: absolute;
  right: 12rpx;
  bottom: 12rpx;
  padding: 8rpx 14rpx;
  border-radius: 999rpx;
  background: rgba(7, 17, 31, 0.72);
  font-size: 20rpx;
}
</style>
