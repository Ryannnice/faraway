<script setup>
import { ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";

import { getContentDetail } from "@/api/content";
import { resolveAssetUrl } from "@/api/request";
import AppNavBar from "@/components/AppNavBar.vue";
import { ROUTES } from "@/constants/routes";
import { ensureLoggedIn, useAuthGuard } from "@/composables/useAuthGuard";
import { formatDateTime } from "@/utils/format";
import { go } from "@/utils/navigation";

useAuthGuard();

const detail = ref(null);

onLoad(async (options) => {
  if (!ensureLoggedIn()) {
    return;
  }
  const contentId = options && options.content_id ? options.content_id : "";
  if (!contentId) {
    uni.showToast({ title: "缺少内容 ID", icon: "none" });
    return;
  }
  try {
    detail.value = await getContentDetail(contentId);
  } catch (error) {
    uni.showToast({
      title: error instanceof Error ? error.message : "加载失败",
      icon: "none",
    });
  }
});

function openAuthorProfile() {
  if (!detail.value || !detail.value.author) {
    return;
  }
  go(`${ROUTES.userProfile}?user_id=${detail.value.author.user_id}`);
}
</script>

<template>
  <view class="page-shell">
    <AppNavBar title="内容详情" subtitle="Content Detail" />

    <view v-if="detail" class="card-stack">
      <view class="glass-card panel">
        <image v-if="detail.cover_url" class="cover-image" :src="resolveAssetUrl(detail.cover_url)" mode="aspectFill" />
        <view class="tag-row">
          <text v-for="tag in detail.tags" :key="tag" class="tag-chip">{{ tag }}</text>
        </view>
        <text class="panel-title">{{ detail.title }}</text>
        <view class="author-row" @tap="openAuthorProfile">
          <image
            v-if="detail.author.avatar"
            class="author-avatar"
            :src="resolveAssetUrl(detail.author.avatar)"
            mode="aspectFill"
          />
          <view v-else class="author-fallback">{{ detail.author.nickname.slice(0, 1) }}</view>
          <view>
            <text class="author-name">{{ detail.author.nickname }}</text>
            <text class="author-time">{{ formatDateTime(detail.published_at) }}</text>
          </view>
        </view>
      </view>

      <view v-if="detail.content_type === 'strategy'" class="glass-card panel">
        <text class="section-kicker">Strategy</text>
        <text class="body-copy">{{ detail.overview }}</text>

        <view v-for="day in detail.daily_plans || []" :key="day.day" class="day-card">
          <text class="day-title">Day {{ day.day }}</text>
          <text class="day-block">活动：{{ day.activities.join(" / ") }}</text>
          <text class="day-block">餐食：{{ day.food.join(" / ") }}</text>
          <text class="day-block">住宿：{{ day.accommodation }}</text>
        </view>

        <view v-if="detail.tips && detail.tips.length" class="tips-card">
          <text class="day-title">Tips</text>
          <text v-for="tip in detail.tips" :key="tip" class="day-block">{{ tip }}</text>
        </view>
      </view>

      <view v-else class="glass-card panel">
        <text class="section-kicker">Graphic Post</text>
        <text class="body-copy">{{ detail.content }}</text>
        <view v-if="detail.image_urls && detail.image_urls.length" class="image-grid">
          <image
            v-for="(url, index) in detail.image_urls"
            :key="`${url}-${index}`"
            class="detail-image"
            :src="resolveAssetUrl(url)"
            mode="aspectFill"
          />
        </view>
      </view>
    </view>
  </view>
</template>

<style scoped lang="scss">
.panel {
  border-radius: 34rpx;
  padding: 30rpx;
}

.cover-image {
  width: 100%;
  height: 360rpx;
  border-radius: 24rpx;
}

.tag-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
  margin-top: 20rpx;
}

.panel-title {
  display: block;
  margin-top: 20rpx;
  font-size: 40rpx;
  font-weight: 700;
}

.author-row {
  display: flex;
  align-items: center;
  gap: 16rpx;
  margin-top: 22rpx;
}

.author-avatar,
.author-fallback {
  width: 72rpx;
  height: 72rpx;
  border-radius: 999rpx;
}

.author-fallback {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(236, 214, 179, 0.18);
}

.author-name,
.author-time,
.body-copy,
.day-block {
  display: block;
}

.author-time,
.day-block {
  color: rgba(246, 240, 232, 0.68);
}

.body-copy {
  margin-top: 18rpx;
  line-height: 1.8;
  color: rgba(246, 240, 232, 0.76);
}

.day-card,
.tips-card {
  margin-top: 22rpx;
  padding: 24rpx;
  border-radius: 24rpx;
  background: rgba(255, 255, 255, 0.05);
}

.day-title {
  display: block;
  font-weight: 700;
  margin-bottom: 12rpx;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16rpx;
  margin-top: 22rpx;
}

.detail-image {
  width: 100%;
  height: 280rpx;
  border-radius: 20rpx;
}
</style>
