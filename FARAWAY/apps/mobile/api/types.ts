export interface ApiEnvelope<T> {
  code: number;
  message: string;
  data: T;
}

export interface UserInfo {
  id: string;
  nickname: string;
  avatar: string;
}

export interface UserProfile extends UserInfo {
  bio: string;
  gender: "unknown" | "male" | "female";
  created_at: string;
  updated_at: string;
}

export interface StrategyResult {
  destination: string;
  overview: string;
  daily_plans: Array<{
    day: number;
    activities: string[];
    food: string[];
    accommodation: string;
  }>;
  tips: string[];
}

export interface MatchCandidateView {
  candidate_id: string;
  peer_user_id: string;
  peer_nickname: string;
  peer_avatar: string;
  meeting_place_text: string;
  match_summary: string;
  decision_expires_at: string;
  my_decision: "pending" | "accepted" | "rejected";
  peer_decision: "pending" | "accepted" | "rejected";
}

export interface MatchPairView {
  pair_id: string;
  status: "active" | "finished";
  peer_user_id: string;
  peer_nickname: string;
  peer_avatar: string;
  meet_time: string;
  meet_location_text: string;
  my_remark: string;
  peer_remark: string;
}

export interface CurrentMatchState {
  active: boolean;
  request_id: string | null;
  status: string | null;
  destination?: string;
  travel_start_date?: string;
  travel_end_date?: string;
  preference_tags?: string[];
  preference_text?: string;
  match_deadline_at?: string;
  candidate: MatchCandidateView | null;
  pair: MatchPairView | null;
}

export interface NotificationItem {
  id: string;
  type: string;
  title: string;
  content: string;
  payload: Record<string, string>;
  created_at: string;
  updated_at: string;
}
