import { request } from "./request";
import type { StrategyResult } from "./types";

export function generateStrategy(payload: {
  destination: string;
  days: number;
  budget: string;
  hotel_requirement: string;
  allergies: string;
  pace: string;
  group_type: string;
}) {
  return request<StrategyResult>({
    url: "/api/ai/generate-strategy",
    method: "POST",
    data: payload,
  });
}
