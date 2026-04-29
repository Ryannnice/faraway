import { request } from "./request";
import type {
  ContentDetail,
  ContentFeedResponse,
  ContentSummary,
  StrategyPublishPayload,
  VlogPublishPayload,
} from "./types";

export function publishStrategy(payload: StrategyPublishPayload) {
  return request<ContentSummary>({
    url: "/api/content/strategy/publish",
    method: "POST",
    data: payload,
  });
}

export function publishVlog(payload: VlogPublishPayload) {
  return request<ContentSummary>({
    url: "/api/content/vlog/publish",
    method: "POST",
    data: payload,
  });
}

export function getContentFeed(page = 1, pageSize = 20) {
  return request<ContentFeedResponse>({
    url: "/api/content/feed",
    data: {
      page,
      page_size: pageSize,
    },
  });
}

export function getContentDetail(contentId: string) {
  return request<ContentDetail>({
    url: `/api/content/${contentId}`,
  });
}

export function getMyContents(page = 1, pageSize = 20) {
  return request<ContentFeedResponse>({
    url: "/api/my/contents",
    data: {
      page,
      page_size: pageSize,
    },
  });
}
