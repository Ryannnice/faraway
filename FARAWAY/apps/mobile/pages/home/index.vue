<script setup>
import { computed, ref } from "vue";
import { onShow } from "@dcloudio/uni-app";

import { getContentFeed } from "@/api/content";
import { resolveAssetUrl } from "@/api/request";
import AppNavBar from "@/components/AppNavBar.vue";
import { ROUTES } from "@/constants/routes";
import { ensureLoggedIn, useAuthGuard } from "@/composables/useAuthGuard";
import { useAuthStore } from "@/stores/auth";
import { formatDateTime } from "@/utils/format";
import { go } from "@/utils/navigation";

useAuthGuard();

const authStore = useAuthStore();
const nickname = computed(() => {
  const userInfo = authStore.userInfo;
  return userInfo && userInfo.nickname ? userInfo.nickname : "旅人";
});
const heroImage =
  "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&q=80&w=2000";
const feed = ref([]);
const page = ref(1);
const hasMore = ref(true);
const loadingFeed = ref(false);

async function loadFeed(reset) {
  if (!ensureLoggedIn() || loadingFeed.value) {
    return;
  }
  loadingFeed.value = true;
  const nextPage = reset ? 1 : page.value;
  try {
    const data = await getContentFeed(nextPage, 20);
    feed.value = reset ? data.list : feed.value.concat(data.list);
    page.value = nextPage + 1;
    hasMore.value = data.has_more;
  } catch (error) {
    uni.showToast({
      title: error instanceof Error ? error.message : "加载失败",
      icon: "none",
    });
  } finally {
    loadingFeed.value = false;
  }
}

function openPublishActions() {
  uni.showActionSheet({
    itemList: ["发布攻略", "发图文"],
    success: (result) => {
      if (result.tapIndex === 0) {
        go(ROUTES.strategy);
        return;
      }
      go(ROUTES.publishText);
    },
  });
}

function openContentDetail(item) {
  go(`${ROUTES.contentDetail}?content_id=${item.content_id}`);
}

onShow(() => {
  if (!ensureLoggedIn()) {
    return;
  }
  authStore.hydrate();
  void loadFeed(true);
});
</script>

<template>
  <view class="home-page">
    <image class="hero-bg" :src="heroImage" mode="aspectFill" />
    <view class="hero-mask" />

    <view class="hero-content">
      <AppNavBar title="Faraway" subtitle="Home Feed" :backable="false" />
      <text class="section-kicker">Faraway Polaris</text>
      <text class="hero-title">你好，{{ nickname }}。</text>
      <text class="hero-copy">先决定怎么出发，再决定和谁一起出发。</text>

      <view class="cta-row">
        <view class="pill-button cta" @tap="go(ROUTES.strategy)">做攻略</view>
        <view class="pill-button cta accent" @tap="go(ROUTES.match)">找搭子</view>
      </view>

      <view class="quick-links glass-card">
        <view class="quick-link" @tap="go(ROUTES.myContents)">
          <text class="quick-title">我的内容</text>
          <text class="quick-copy">查看已发布的攻略和图文</text>
        </view>
        <view class="quick-link" @tap="go(ROUTES.myPartners)">
          <text class="quick-title">我的搭子</text>
          <text class="quick-copy">查看当前匹配和已确认赴约</text>
        </view>
        <view class="quick-link" @tap="go(ROUTES.notice)">
          <text class="quick-title">通知</text>
          <text class="quick-copy">候选出现和确认成功都会留痕</text>
        </view>
        <view class="quick-link" @tap="go(ROUTES.profile)">
          <text class="quick-title">个人资料</text>
          <text class="quick-copy">头像、昵称、简介都在这里维护</text>
        </view>
      </view>

      <view class="feed-section">
        <text class="section-kicker">Public Feed</text>
        <text class="feed-title">最新发布</text>

        <view v-if="feed.length" class="card-stack feed-stack">
          <view v-for="item in feed" :key="item.content_id" class="glass-card feed-card" @tap="openContentDetail(item)">
            <image v-if="item.cover_url" class="feed-cover" :src="resolveAssetUrl(item.cover_url)" mode="aspectFill" />
            <view class="feed-body">
              <view class="tag-row">
                <text v-for="tag in item.tags" :key="tag" class="tag-chip">{{ tag }}</text>
              </view>
              <text class="feed-card-title">{{ item.title }}</text>
              <text class="feed-summary">{{ item.summary }}</text>
              <view class="author-row">
                <image
                  v-if="item.author.avatar"
                  class="author-avatar"
                  :src="resolveAssetUrl(item.author.avatar)"
                  mode="aspectFill"
                />
                <view v-else class="author-fallback">{{ item.author.nickname.slice(0, 1) }}</view>
                <view class="author-copy">
                  <text class="author-name">{{ item.author.nickname }}</text>
                  <text class="author-time">{{ formatDateTime(item.published_at) }}</text>
                </view>
              </view>
            </view>
          </view>

          <button v-if="hasMore" class="secondary-button more-button" @tap="loadFeed(false)">
            {{ loadingFeed ? "加载中..." : "加载更多" }}
          </button>
        </view>

        <view v-else class="glass-card empty-card">
          <text class="feed-card-title">还没有公开内容</text>
          <text class="feed-summary">先去生成一份攻略，或者发第一篇图文。</text>
        </view>
      </view>
    </view>

    <view class="publish-fab" @tap="openPublishActions">发布</view>
  </view>
</template>

<style scoped lang="scss">
.home-page {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

.hero-bg,
.hero-mask {
  position: absolute;
  inset: 0;
}

.hero-bg {
  width: 100%;
  height: 88vh;
}

.hero-mask {
  background: linear-gradient(180deg, rgba(7, 17, 31, 0.08) 0%, rgba(7, 17, 31, 0.28) 44%, #07111f 100%);
}

.hero-content {
  position: relative;
  z-index: 2;
  padding: 28rpx 28rpx 140rpx;
}

.hero-title,
.feed-title {
  display: block;
  margin-top: 24rpx;
  font-size: 64rpx;
  line-height: 1.08;
  font-weight: 700;
  color: #f6f0e8;
}

.feed-title {
  font-size: 42rpx;
}

.hero-copy {
  display: block;
  margin-top: 24rpx;
  width: 78%;
  font-size: 30rpx;
  line-height: 1.6;
  color: rgba(246, 240, 232, 0.72);
}

.cta-row {
  display: flex;
  gap: 20rpx;
  margin-top: 36rpx;
}

.cta {
  min-width: 200rpx;
}

.accent {
  background: rgba(236, 214, 179, 0.18);
}

.quick-links {
  margin-top: 56rpx;
  border-radius: 34rpx;
  padding: 20rpx 28rpx;
}

.quick-link {
  padding: 24rpx 0;
  border-bottom: 1rpx solid rgba(255, 255, 255, 0.08);
}

.quick-link:last-child {
  border-bottom: none;
}

.quick-title {
  display: block;
  font-size: 30rpx;
  font-weight: 700;
}

.quick-copy {
  display: block;
  margin-top: 10rpx;
  font-size: 24rpx;
  color: rgba(246, 240, 232, 0.68);
}

.feed-section {
  margin-top: 56rpx;
}

.feed-stack {
  margin-top: 26rpx;
}

.feed-card,
.empty-card {
  border-radius: 34rpx;
  overflow: hidden;
}

.feed-cover {
  width: 100%;
  height: 320rpx;
}

.feed-body,
.empty-card {
  padding: 28rpx;
}

.tag-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.feed-card-title {
  display: block;
  margin-top: 18rpx;
  font-size: 34rpx;
  font-weight: 700;
}

.feed-summary {
  display: block;
  margin-top: 14rpx;
  color: rgba(246, 240, 232, 0.72);
  line-height: 1.7;
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
.author-time {
  display: block;
}

.author-time {
  margin-top: 6rpx;
  color: rgba(246, 240, 232, 0.46);
  font-size: 22rpx;
}

.more-button {
  margin-top: 6rpx;
}

.publish-fab {
  position: fixed;
  right: 28rpx;
  bottom: 48rpx;
  z-index: 5;
  width: 124rpx;
  height: 124rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ecd6b3;
  color: #0c1320;
  font-size: 28rpx;
  font-weight: 700;
  box-shadow: 0 20rpx 60rpx rgba(0, 0, 0, 0.28);
}
</style>
