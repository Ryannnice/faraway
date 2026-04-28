import { backendFirst } from '../request'
import { strategies, vlogs } from '../mock-data'

export function getHomeRecommendBlocks() {
  return backendFirst({
    url: '/api/home/recommend-blocks',
    method: 'GET'
  }, () => ({
    recommendStrategies: strategies.slice(0, 2),
    recommendVlogs: vlogs.slice(0, 2)
  }))
}

export function getHomeFeed() {
  return backendFirst({
    url: '/api/home/feed',
    method: 'GET'
  }, () => ({
    list: [
      ...strategies.slice(0, 2).map((item) => ({ ...item, contentType: 'strategy' })),
      ...vlogs.slice(0, 2).map((item) => ({ ...item, contentType: 'vlog' }))
    ]
  }))
}
