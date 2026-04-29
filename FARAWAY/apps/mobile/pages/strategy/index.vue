<script setup>
import { reactive, ref } from "vue";

import { generateStrategy } from "@/api/ai";
import { publishStrategy } from "@/api/content";
import { resolveAssetUrl, uploadImage } from "@/api/request";
import AppNavBar from "@/components/AppNavBar.vue";
import { ROUTES } from "@/constants/routes";
import { useAuthGuard } from "@/composables/useAuthGuard";
import { go } from "@/utils/navigation";

useAuthGuard();

const form = reactive({
  destination: "",
  days: 3,
  budget: "",
  hotel_requirement: "",
  allergies: "",
  pace: "",
  group_type: "",
});

const result = ref(null);
const generating = ref(false);
const publishing = ref(false);
const publishForm = reactive({
  title: "",
  tagsText: "",
  cover_image: "",
  cover_url: "",
  overview: "",
  tipsText: "",
  daily_plans: [],
});

function resetPublishState() {
  result.value = null;
  publishForm.title = "";
  publishForm.tagsText = "";
  publishForm.cover_image = "";
  publishForm.cover_url = "";
  publishForm.overview = "";
  publishForm.tipsText = "";
  publishForm.daily_plans = [];
}

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

function normalizeLines(text) {
  return text
    .split("\n")
    .map((item) => item.trim())
    .filter(Boolean);
}

function applyResultToPublishState(data) {
  publishForm.title = `${data.destination}${data.daily_plans.length}天攻略`;
  publishForm.tagsText = "";
  publishForm.cover_image = "";
  publishForm.cover_url = "";
  publishForm.overview = data.overview;
  publishForm.tipsText = (data.tips || []).join("\n");
  publishForm.daily_plans = data.daily_plans.map((day) => ({
    day: day.day,
    accommodation: day.accommodation,
    activities_text: day.activities.join("\n"),
    food_text: day.food.join("\n"),
  }));
}

async function handleGenerate() {
  if (generating.value) {
    return;
  }
  generating.value = true;
  try {
    const data = await generateStrategy(form);
    result.value = data;
    applyResultToPublishState(data);
  } catch (error) {
    uni.showToast({
      title: error instanceof Error ? error.message : "生成失败",
      icon: "none",
    });
  } finally {
    generating.value = false;
  }
}

async function chooseCover() {
  try {
    const filePath = await new Promise((resolve, reject) => {
      uni.chooseImage({
        count: 1,
        success: (picked) => resolve(picked.tempFilePaths[0]),
        fail: reject,
      });
    });
    const uploaded = await uploadImage(filePath);
    publishForm.cover_image = uploaded.asset_id;
    publishForm.cover_url = uploaded.url;
  } catch (error) {
    uni.showToast({
      title: error instanceof Error ? error.message : "上传失败",
      icon: "none",
    });
  }
}

function confirmPublish() {
  if (!result.value || publishing.value) {
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
        const published = await publishStrategy({
          title: publishForm.title,
          tags: normalizeTags(publishForm.tagsText),
          cover_asset_id: publishForm.cover_image || null,
          destination: result.value.destination,
          days: result.value.daily_plans.length,
          overview: publishForm.overview,
          daily_plans: publishForm.daily_plans.map((day) => ({
            day: day.day,
            activities: normalizeLines(day.activities_text),
            food: normalizeLines(day.food_text),
            accommodation: day.accommodation,
          })),
          tips: normalizeLines(publishForm.tipsText),
        });
        resetPublishState();
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
    <AppNavBar title="AI 攻略" subtitle="Strategy Publish" />

    <view class="card-stack">
      <view class="glass-card panel">
        <text class="section-kicker">Plan Input</text>
        <text class="panel-title">告诉 AI 你这次要怎么走。</text>

        <view class="field-block">
          <text class="label-text">目的地</text>
          <input v-model="form.destination" class="field-input" placeholder="例如：京都、大理、伊斯坦布尔" />
        </view>

        <view class="field-block">
          <text class="label-text">天数</text>
          <input v-model.number="form.days" class="field-input" type="number" />
        </view>

        <view class="field-block">
          <text class="label-text">预算</text>
          <input v-model="form.budget" class="field-input" placeholder="例如：中等" />
        </view>

        <view class="field-block">
          <text class="label-text">酒店偏好</text>
          <input v-model="form.hotel_requirement" class="field-input" placeholder="例如：近地铁、安静一点" />
        </view>

        <view class="field-block">
          <text class="label-text">忌口 / 过敏</text>
          <input v-model="form.allergies" class="field-input" placeholder="例如：不吃海鲜" />
        </view>

        <view class="field-block">
          <text class="label-text">节奏</text>
          <input v-model="form.pace" class="field-input" placeholder="例如：慢一点" />
        </view>

        <view class="field-block">
          <text class="label-text">出行类型</text>
          <input v-model="form.group_type" class="field-input" placeholder="例如：自由行" />
        </view>

        <button class="primary-button submit-button" :class="{ 'button-disabled': generating }" @tap="handleGenerate">
          {{ generating ? "生成中..." : "生成攻略" }}
        </button>
      </view>

      <view v-if="result" class="glass-card panel">
        <text class="section-kicker">Strategy Result</text>
        <text class="panel-title">{{ result.destination }}</text>

        <view class="field-block">
          <text class="label-text">发布标题</text>
          <input v-model="publishForm.title" class="field-input" maxlength="60" />
        </view>

        <view class="field-block">
          <text class="label-text">业务标签</text>
          <input v-model="publishForm.tagsText" class="field-input" placeholder="例如：赏樱, 慢游, 美食" />
        </view>

        <view class="field-block">
          <text class="label-text">封面图</text>
          <view class="cover-block">
            <image
              v-if="publishForm.cover_url"
              class="cover-preview"
              :src="resolveAssetUrl(publishForm.cover_url)"
              mode="aspectFill"
            />
            <view v-else class="cover-empty">未上传封面</view>
            <button class="secondary-button cover-button" @tap="chooseCover">上传封面</button>
          </view>
        </view>

        <view class="field-block">
          <text class="label-text">概述</text>
          <textarea v-model="publishForm.overview" class="field-textarea" maxlength="1000" />
        </view>

        <view v-for="day in publishForm.daily_plans" :key="day.day" class="day-card">
          <text class="day-title">Day {{ day.day }}</text>

          <view class="field-block">
            <text class="label-text">活动</text>
            <textarea v-model="day.activities_text" class="field-textarea day-textarea" />
          </view>

          <view class="field-block">
            <text class="label-text">餐食</text>
            <textarea v-model="day.food_text" class="field-textarea day-textarea" />
          </view>

          <view class="field-block">
            <text class="label-text">住宿</text>
            <input v-model="day.accommodation" class="field-input" />
          </view>
        </view>

        <view class="field-block">
          <text class="label-text">Tips（每行一条）</text>
          <textarea v-model="publishForm.tipsText" class="field-textarea" />
        </view>

        <view class="action-row">
          <button class="secondary-button row-button" @tap="handleGenerate">重新生成</button>
          <button class="danger-button row-button" @tap="resetPublishState">放弃</button>
        </view>
        <button class="primary-button publish-button" :class="{ 'button-disabled': publishing }" @tap="confirmPublish">
          {{ publishing ? "发布中..." : "发布攻略" }}
        </button>
      </view>
    </view>
  </view>
</template>

<style scoped lang="scss">
.panel {
  border-radius: 34rpx;
  padding: 30rpx;
}

.panel-title {
  display: block;
  margin-top: 12rpx;
  font-size: 38rpx;
  font-weight: 700;
}

.field-block {
  margin-top: 20rpx;
}

.submit-button,
.publish-button {
  margin-top: 28rpx;
}

.cover-block {
  display: flex;
  flex-direction: column;
  gap: 18rpx;
}

.cover-preview,
.cover-empty {
  width: 100%;
  height: 280rpx;
  border-radius: 24rpx;
}

.cover-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  color: rgba(246, 240, 232, 0.52);
}

.day-card {
  margin-top: 22rpx;
  padding: 24rpx;
  border-radius: 24rpx;
  background: rgba(255, 255, 255, 0.05);
}

.day-title {
  display: block;
  font-weight: 700;
}

.day-textarea {
  min-height: 160rpx;
}

.action-row {
  display: flex;
  gap: 16rpx;
  margin-top: 28rpx;
}

.row-button {
  flex: 1;
}
</style>
