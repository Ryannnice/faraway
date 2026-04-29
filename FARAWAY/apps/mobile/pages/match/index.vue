<script setup lang="ts">
import { computed, onBeforeUnmount, reactive, ref } from "vue";
import { onHide, onShow } from "@dcloudio/uni-app";

import AppNavBar from "@/components/AppNavBar.vue";
import { MATCH_PREFERENCE_TAGS, MATCH_STATUS_LABELS } from "@/constants/match";
import { ROUTES } from "@/constants/routes";
import { useAuthGuard } from "@/composables/useAuthGuard";
import { useMatchStore } from "@/stores/match";
import { formatDate, formatDateTime } from "@/utils/format";
import { go } from "@/utils/navigation";
import { markCandidateSeen, readSeenCandidateIds } from "@/utils/storage";

useAuthGuard();

const matchStore = useMatchStore();
const current = computed(() => matchStore.current);
const loading = ref(false);
const editing = ref(false);
const remarkText = ref("");
let timer: ReturnType<typeof setInterval> | null = null;

function addDays(days: number): string {
  const date = new Date();
  date.setDate(date.getDate() + days);
  const year = date.getFullYear();
  const month = `${date.getMonth() + 1}`.padStart(2, "0");
  const day = `${date.getDate()}`.padStart(2, "0");
  return `${year}-${month}-${day}`;
}

const form = reactive({
  destination: "",
  travel_start_date: addDays(5),
  travel_end_date: addDays(7),
  preference_tags: [] as string[],
  preference_text: "",
});

const terminalStatuses = new Set(["failed", "cancelled", "finished"]);
const currentStatus = computed(() => current.value?.status || null);

const viewMode = computed(() => {
  if (!currentStatus.value) {
    return "form";
  }
  if (editing.value) {
    return "form";
  }
  if (currentStatus.value === "pending") {
    return "pending";
  }
  if (currentStatus.value === "matched_waiting_decision") {
    return "waiting";
  }
  if (currentStatus.value === "matched_accepted") {
    return "accepted";
  }
  if (terminalStatuses.has(currentStatus.value)) {
    return "ended";
  }
  return "form";
});

function syncFormFromCurrent() {
  if (!current.value) {
    return;
  }
  form.destination = current.value.destination || "";
  form.travel_start_date = current.value.travel_start_date || addDays(5);
  form.travel_end_date = current.value.travel_end_date || addDays(7);
  form.preference_tags = [...(current.value.preference_tags || [])];
  form.preference_text = current.value.preference_text || "";
}

async function refreshCurrent() {
  try {
    await matchStore.fetchCurrent();
    if (current.value?.status === "matched_waiting_decision" && current.value.candidate) {
      const candidateId = current.value.candidate.candidate_id;
      if (!readSeenCandidateIds().includes(candidateId)) {
        markCandidateSeen(candidateId);
        uni.showModal({
          title: "找到候选搭子",
          content: `${current.value.candidate.peer_nickname} 出现了，去决定是否同意赴约。`,
          showCancel: false,
        });
      }
    }
  } catch (error) {
    uni.showToast({
      title: error instanceof Error ? error.message : "刷新失败",
      icon: "none",
    });
  }
}

function startPolling() {
  stopPolling();
  timer = setInterval(() => {
    void refreshCurrent();
  }, 5000);
}

function stopPolling() {
  if (timer) {
    clearInterval(timer);
    timer = null;
  }
}

onShow(async () => {
  await refreshCurrent();
  startPolling();
});

onHide(() => {
  stopPolling();
});

onBeforeUnmount(() => {
  stopPolling();
});

function toggleTag(tag: string) {
  if (form.preference_tags.includes(tag)) {
    form.preference_tags = form.preference_tags.filter((item) => item !== tag);
    return;
  }
  form.preference_tags = [...form.preference_tags, tag];
}

function beginEdit() {
  syncFormFromCurrent();
  editing.value = true;
}

function restartFlow() {
  form.destination = "";
  form.travel_start_date = addDays(5);
  form.travel_end_date = addDays(7);
  form.preference_tags = [];
  form.preference_text = "";
  editing.value = true;
}

async function submitRequest() {
  if (loading.value) {
    return;
  }
  loading.value = true;
  try {
    await matchStore.create({ ...form });
    editing.value = false;
    await refreshCurrent();
  } catch (error) {
    uni.showToast({
      title: error instanceof Error ? error.message : "提交失败",
      icon: "none",
    });
  } finally {
    loading.value = false;
  }
}

async function cancelRequest() {
  if (!current.value?.request_id) {
    return;
  }
  await matchStore.cancel(current.value.request_id);
}

async function acceptCandidate() {
  const candidateId = current.value?.candidate?.candidate_id;
  if (!candidateId) {
    return;
  }
  await matchStore.accept(candidateId);
}

async function rejectCandidate() {
  const candidateId = current.value?.candidate?.candidate_id;
  if (!candidateId) {
    return;
  }
  await matchStore.reject(candidateId);
}

async function submitRemark() {
  const pairId = current.value?.pair?.pair_id;
  if (!pairId || !remarkText.value.trim()) {
    return;
  }
  await matchStore.remark(pairId, remarkText.value.trim());
  remarkText.value = "";
}
</script>

<template>
  <view class="page-shell">
    <AppNavBar title="找搭子" subtitle="Realtime Match" />

    <view class="hero-card glass-card">
      <text class="section-kicker">Realtime Match</text>
      <text class="hero-title">填完条件，系统会替你持续找人。</text>
      <text class="hero-copy">页面以服务端状态为准，轮询间隔固定 5 秒。</text>
    </view>

    <view v-if="viewMode === 'form'" class="card-stack">
      <view class="glass-card panel">
        <view class="field-block">
          <text class="label-text">目的地</text>
          <input v-model="form.destination" class="field-input" placeholder="例如：大阪、大理、冰岛" />
        </view>
        <view class="field-block">
          <text class="label-text">开始日期</text>
          <input v-model="form.travel_start_date" class="field-input" />
        </view>
        <view class="field-block">
          <text class="label-text">结束日期</text>
          <input v-model="form.travel_end_date" class="field-input" />
        </view>
        <view class="field-block">
          <text class="label-text">偏好标签</text>
          <view class="tag-grid">
            <view
              v-for="tag in MATCH_PREFERENCE_TAGS"
              :key="tag"
              class="tag-option"
              :class="{ active: form.preference_tags.includes(tag) }"
              @tap="toggleTag(tag)"
            >
              {{ tag }}
            </view>
          </view>
        </view>
        <view class="field-block">
          <text class="label-text">补充说明</text>
          <textarea v-model="form.preference_text" class="field-textarea" maxlength="200" />
        </view>
        <button class="primary-button action-button" :class="{ 'button-disabled': loading }" @tap="submitRequest">
          {{ loading ? "提交中..." : currentStatus === 'pending' ? '覆盖当前匹配条件' : '开始匹配' }}
        </button>
      </view>
    </view>

    <view v-else-if="viewMode === 'pending'" class="card-stack">
      <view class="glass-card panel">
        <text class="panel-title">{{ MATCH_STATUS_LABELS.pending }}</text>
        <text class="panel-copy">目的地：{{ current?.destination }}</text>
        <text class="panel-copy">日期：{{ formatDate(current?.travel_start_date) }} - {{ formatDate(current?.travel_end_date) }}</text>
        <text class="panel-copy">截止：{{ formatDateTime(current?.match_deadline_at) }}</text>
        <view class="tag-row">
          <text v-for="tag in current?.preference_tags || []" :key="tag" class="tag-chip">{{ tag }}</text>
        </view>
        <text v-if="current?.preference_text" class="panel-copy">{{ current.preference_text }}</text>
      </view>
      <button class="secondary-button action-button" @tap="beginEdit">重新填写条件</button>
      <button class="danger-button action-button" @tap="cancelRequest">取消匹配</button>
    </view>

    <view v-else-if="viewMode === 'waiting'" class="card-stack">
      <view class="glass-card panel">
        <text class="panel-title">候选搭子：{{ current?.candidate?.peer_nickname }}</text>
        <text class="panel-copy">截止：{{ formatDateTime(current?.candidate?.decision_expires_at) }}</text>
        <text class="panel-copy">匹配理由：{{ current?.candidate?.match_summary }}</text>
        <text class="panel-copy">建议见面地：{{ current?.candidate?.meeting_place_text }}</text>
        <text class="panel-copy" v-if="current?.candidate?.my_decision === 'accepted'">你已经同意，正在等待对方回应。</text>
      </view>
      <button class="secondary-button action-button" @tap="go(`${ROUTES.userProfile}?user_id=${current?.candidate?.peer_user_id}`)">查看 TA 的主页</button>
      <view v-if="current?.candidate?.my_decision !== 'accepted'" class="action-row">
        <button class="secondary-button row-button" @tap="rejectCandidate">拒绝，继续寻找</button>
        <button class="primary-button row-button" @tap="acceptCandidate">我愿意</button>
      </view>
    </view>

    <view v-else-if="viewMode === 'accepted'" class="card-stack">
      <view class="glass-card panel">
        <text class="panel-title">已确认赴约：{{ current?.pair?.peer_nickname }}</text>
        <text class="panel-copy">见面时间：{{ formatDateTime(current?.pair?.meet_time) }}</text>
        <text class="panel-copy">见面地点：{{ current?.pair?.meet_location_text }}</text>
        <text class="panel-copy">对方备注：{{ current?.pair?.peer_remark || "对方还没填写备注。" }}</text>
        <text class="panel-copy" v-if="current?.pair?.my_remark">我的备注：{{ current.pair.my_remark }}</text>
      </view>
      <view v-if="current?.pair && !current.pair.my_remark" class="glass-card panel">
        <text class="label-text">我的备注（只能发送一次）</text>
        <textarea v-model="remarkText" class="field-textarea" maxlength="200" />
        <button class="primary-button action-button" @tap="submitRemark">提交备注</button>
      </view>
    </view>

    <view v-else-if="viewMode === 'ended'" class="card-stack">
      <view class="glass-card panel">
        <text class="panel-title">{{ currentStatus ? MATCH_STATUS_LABELS[currentStatus] : "已结束" }}</text>
        <text class="panel-copy">上一轮请求已经结束，你可以重新开始下一轮。</text>
      </view>
      <button class="primary-button action-button" @tap="restartFlow">重新开始</button>
    </view>
  </view>
</template>

<style scoped lang="scss">
.hero-card,
.panel {
  border-radius: 34rpx;
  padding: 30rpx;
}

.hero-title,
.panel-title {
  display: block;
  margin-top: 12rpx;
  font-size: 36rpx;
  font-weight: 700;
}

.hero-copy,
.panel-copy {
  display: block;
  margin-top: 16rpx;
  color: rgba(246, 240, 232, 0.72);
  line-height: 1.7;
}

.field-block {
  margin-top: 20rpx;
}

.tag-grid,
.tag-row {
  display: flex;
  flex-wrap: wrap;
  gap: 14rpx;
}

.tag-option {
  padding: 14rpx 18rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.06);
  color: rgba(246, 240, 232, 0.72);
}

.tag-option.active {
  background: rgba(236, 214, 179, 0.18);
  color: #f6f0e8;
}

.action-button {
  margin-top: 24rpx;
}

.action-row {
  display: flex;
  gap: 16rpx;
}

.row-button {
  flex: 1;
  margin-top: 0;
}
</style>
