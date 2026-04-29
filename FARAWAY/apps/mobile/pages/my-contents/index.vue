<script setup>
import { ref } from "vue";
import { onShow } from "@dcloudio/uni-app";

import { getMyContents } from "@/api/content";
import { resolveAssetUrl } from "@/api/request";
import AppNavBar from "@/components/AppNavBar.vue";
import { ROUTES } from "@/constants/routes";
import { ensureLoggedIn, useAuthGuard } from "@/composables/useAuthGuard";
import { formatDateTime } from "@/utils/format";
import { go } from "@/utils/navigation";

useAuthGuard();

const list = ref([]);
const page = ref(1);
const hasMore = ref(true);
const loading = ref(false);

async function loadContents(reset) {
  if (!ensureLoggedIn() || loading.value) {
    return;
  }
  loading.value = true;
  const nextPage = reset ? 1 : page.value;
  try {
    const data = await getMyContents(nextPage, 20);
    list.value = reset ? data.list : list.value.concat(data.list);
    page.value = nextPage + 1;
    hasMore.value = data.has_more;
  } catch (error) {
    uni.showToast({
      title: error instanceof Error ? error.message : "加载失败",
      icon: "none",
    });
  } finally {
    loading.value = false;
  }
}

function openDetail(item) {
  go(`${ROUTES.contentDetail}?content_id=${item.content_id}`);
}

onShow(() => {
  void loadContents(true);
});
</script>

<template>
  <view class="page-shell">
    <AppNavBar title="我的内容" subtitle="My Contents" />

    <view v-if="list.length" class="card-stack">
      <view v-for="item in list" :key="item.content_id" class="glass-card card" @tap="openDetail(item)">
        <image v-if="item.cover_url" class="cover-image" :src="resolveAssetUrl(item.cover_url)" mode="aspectFill" />
        <view class="card-body">
          <view class="tag-row">
            <text v-for="tag in item.tags" :key="tag" class="tag-chip">{{ tag }}</text>
          </view>
          <text class="card-title">{{ item.title }}</text>
          <text class="card-summary">{{ item.summary }}</text>
          <text class="card-time">{{ formatDateTime(item.published_at) }}</text>
        </view>
      </view>

      <button v-if="hasMore" class="secondary-button more-button" @tap="loadContents(false)">
        {{ loading ? "加载中..." : "加载更多" }}
      </button>
    </view>

    <view v-else class="glass-card empty-card">
      <text class="card-title">你还没有发布内容</text>
      <text class="card-summary">先去生成一份攻略，或者发第一篇图文。</text>
    </view>
  </view>
</template>

<style scoped lang="scss">
.card,
.empty-card {
  border-radius: 34rpx;
  overflow: hidden;
}

.cover-image {
  width: 100%;
  height: 320rpx;
}

.card-body,
.empty-card {
  padding: 28rpx;
}

.tag-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.card-title {
  display: block;
  margin-top: 16rpx;
  font-size: 34rpx;
  font-weight: 700;
}

.card-summary,
.card-time {
  display: block;
  margin-top: 12rpx;
  color: rgba(246, 240, 232, 0.68);
  line-height: 1.6;
}

.more-button {
  margin-top: 6rpx;
}
</style>
