import { backendFirst } from '../request'
import { hotKeywords, strategies, vlogs } from '../mock-data'

export function searchAll(params = {}) {
  return backendFirst({
    url: '/api/search',
    method: 'GET',
    data: params
  }, () => {
    const keyword = (params.keyword || '').toLowerCase()
    const strategyList = strategies.filter((item) => !keyword || [item.title, item.summary, item.destination, item.tags.join(' ')].join(' ').toLowerCase().includes(keyword))
    const vlogList = vlogs.filter((item) => !keyword || [item.title, item.location, item.tags.join(' '), item.content].join(' ').toLowerCase().includes(keyword))
    if (params.type === 'strategy') {
      return { strategyList, vlogList: [], total: strategyList.length }
    }
    if (params.type === 'vlog') {
      return { strategyList: [], vlogList, total: vlogList.length }
    }
    return { strategyList, vlogList, total: strategyList.length + vlogList.length }
  })
}

export function getHotSearchList() {
  return backendFirst({
    url: '/api/search/hot',
    method: 'GET'
  }, () => ({
    list: hotKeywords.map((keyword, index) => ({
      id: index + 1,
      keyword,
      type: 'destination',
      sort: index + 1
    }))
  }))
}
