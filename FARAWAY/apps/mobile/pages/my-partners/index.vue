<script setup lang="ts">
import { computed } from "vue";
import { onShow } from "@dcloudio/uni-app";

import AppNavBar from "@/components/AppNavBar.vue";
import { MATCH_STATUS_LABELS } from "@/constants/match";
import { ROUTES } from "@/constants/routes";
import { useAuthGuard } from "@/composables/useAuthGuard";
import { useMatchStore } from "@/stores/match";
import { formatDate, formatDateTime } from "@/utils/format";
import { go } from "@/utils/navigation";

useAuthGuard();

const matchStore = useMatchStore();
const current = computed(() => matchStore.current);

onShow(() => {
  void matchStore.fetchCurrent();
});
</script>

<template>
  <view class="page-shell">
    <AppNavBar title="我的搭子" subtitle="Partners" />

    <view class="card-stack">
      <view class="glass-card panel">
        <text class="section-kicker">Current Status</text>
        <text class="panel-title">
          {{ current?.status ? MATCH_STATUS_LABELS[current.status] || current.status : "还没有开始匹配" }}
        </text>
        <text class="muted-text body-copy">
          {{ current?.destination ? `${current.destination} / ${formatDate(current.travel_start_date)} - ${formatDate(current.travel_end_date)}` : "从这里直接进入找搭子主链路。" }}
        </text>
        <button class="primary-button action-button" @tap="go(ROUTES.match)">进入找搭子</button>
      </view>

      <view v-if="current?.pair" class="glass-card panel">
        <text class="section-kicker">Confirmed Pair</text>
        <text class="panel-title">{{ current.pair.peer_nickname }}</text>
        <text class="muted-text body-copy">见面时间：{{ formatDateTime(current.pair.meet_time) }}</text>
        <text class="muted-text body-copy">见面地点：{{ current.pair.meet_location_text }}</text>
      </view>

      <view class="glass-card panel">
        <text class="section-kicker">Notice</text>
        <text class="panel-title">通知页只做只读展示</text>
        <button class="secondary-button action-button" @tap="go(ROUTES.notice)">进入通知页</button>
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
  font-size: 34rpx;
  font-weight: 700;
}

.body-copy {
  display: block;
  margin-top: 18rpx;
  line-height: 1.7;
}

.action-button {
  margin-top: 26rpx;
}
</style>
