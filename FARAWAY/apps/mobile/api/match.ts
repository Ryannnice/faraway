import { request } from "./request";
import type { CurrentMatchState, MatchPairView } from "./types";

export function createRealtimeMatch(payload: {
  destination: string;
  travel_start_date: string;
  travel_end_date: string;
  preference_tags: string[];
  preference_text: string;
}) {
  return request<CurrentMatchState>({
    url: "/api/match/realtime",
    method: "POST",
    data: payload,
  });
}

export function getCurrentRealtimeMatch() {
  return request<CurrentMatchState>({
    url: "/api/match/realtime/current",
  });
}

export function acceptRealtimeCandidate(candidateId: string) {
  return request<Record<string, unknown>>({
    url: `/api/match/realtime/candidate/${candidateId}/accept`,
    method: "POST",
  });
}

export function rejectRealtimeCandidate(candidateId: string) {
  return request<{ status: string }>({
    url: `/api/match/realtime/candidate/${candidateId}/reject`,
    method: "POST",
  });
}

export function submitPairRemark(pairId: string, remark: string) {
  return request<MatchPairView>({
    url: `/api/match/realtime/pair/${pairId}/remark`,
    method: "POST",
    data: { remark },
  });
}

export function cancelRealtimeMatch(requestId: string) {
  return request<{ status: string }>({
    url: `/api/match/realtime/${requestId}/cancel`,
    method: "POST",
  });
}
