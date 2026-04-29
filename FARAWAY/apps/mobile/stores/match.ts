import { defineStore } from "pinia";

import {
  acceptRealtimeCandidate,
  cancelRealtimeMatch,
  createRealtimeMatch,
  getCurrentRealtimeMatch,
  rejectRealtimeCandidate,
  submitPairRemark,
} from "@/api/match";
import type { CurrentMatchState } from "@/api/types";

export const useMatchStore = defineStore("match", {
  state: () => ({
    current: null as CurrentMatchState | null,
  }),
  actions: {
    async fetchCurrent() {
      this.current = await getCurrentRealtimeMatch();
      return this.current;
    },
    async create(payload: {
      destination: string;
      travel_start_date: string;
      travel_end_date: string;
      preference_tags: string[];
      preference_text: string;
    }) {
      this.current = await createRealtimeMatch(payload);
      return this.current;
    },
    async accept(candidateId: string) {
      await acceptRealtimeCandidate(candidateId);
      return this.fetchCurrent();
    },
    async reject(candidateId: string) {
      await rejectRealtimeCandidate(candidateId);
      return this.fetchCurrent();
    },
    async cancel(requestId: string) {
      await cancelRealtimeMatch(requestId);
      return this.fetchCurrent();
    },
    async remark(pairId: string, remark: string) {
      await submitPairRemark(pairId, remark);
      return this.fetchCurrent();
    },
  },
});
