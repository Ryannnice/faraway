<script setup lang="ts">
import { reactive, ref } from "vue";

import AppNavBar from "@/components/AppNavBar.vue";
import { generateStrategy } from "@/api/ai";
import type { StrategyResult } from "@/api/types";
import { useAuthGuard } from "@/composables/useAuthGuard";

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

const result = ref<StrategyResult | null>(null);
const generating = ref(false);

async function handleGenerate() {
  if (generating.value) {
    return;
  }
  generating.value = true;
  try {
    result.value = await generateStrategy(form);
  } catch (error) {
    uni.showToast({
      title: error instanceof Error ? error.message : "生成失败",
      icon: "none",
    });
  } finally {
    generating.value = false;
  }
}
</script>

<template>
  <view class="page-shell">
    <AppNavBar title="AI 攻略" subtitle="Strategy" />

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
        <text class="overview">{{ result.overview }}</text>

        <view v-for="day in result.daily_plans" :key="day.day" class="day-card">
          <text class="day-title">Day {{ day.day }}</text>
          <text class="day-block">活动：{{ day.activities.join(" / ") }}</text>
          <text class="day-block">餐食：{{ day.food.join(" / ") }}</text>
          <text class="day-block">住宿：{{ day.accommodation }}</text>
        </view>

        <view class="tips-card">
          <text class="day-title">Tips</text>
          <text v-for="tip in result.tips" :key="tip" class="tip-text">{{ tip }}</text>
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

.panel-title {
  display: block;
  margin-top: 12rpx;
  font-size: 38rpx;
  font-weight: 700;
}

.field-block {
  margin-top: 20rpx;
}

.submit-button {
  margin-top: 28rpx;
}

.overview {
  display: block;
  margin-top: 20rpx;
  color: rgba(246, 240, 232, 0.76);
  line-height: 1.7;
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

.day-block,
.tip-text {
  display: block;
  margin-top: 8rpx;
  color: rgba(246, 240, 232, 0.74);
  line-height: 1.6;
}
</style>
