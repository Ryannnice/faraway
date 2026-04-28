import { backendFirst } from '../request'
import { currentUser, drafts, interactionState, strategies } from '../mock-data'

function getNextStrategyId() {
  return strategies.reduce((max, item) => Math.max(max, Number(item.id) || 0), 100) + 1
}

function getNextDraftId() {
  return drafts.reduce((max, item) => Math.max(max, Number(item.id) || 0), 0) + 1
}

function getNowLabel() {
  return '刚刚'
}

function enrichStrategy(item) {
  if (!item) {
    return null
  }
  const commentList = interactionState.strategyComments[item.id] || []
  return {
    ...item,
    isLiked: interactionState.likedStrategies.includes(item.id),
    isFavorited: interactionState.favoritedStrategies.includes(item.id),
    commentCount: commentList.length,
    shareCount: interactionState.strategyShareCount[item.id] || 0
  }
}

export function getStrategyList(params = {}) {
  return backendFirst({
    url: '/api/strategies',
    method: 'GET',
    data: params
  }, () => {
    let list = [...strategies]
    if (params.category && params.category !== '全部') {
      list = list.filter((item) => item.category === params.category)
    }
    if (params.keyword) {
      const keyword = params.keyword.toLowerCase()
      list = list.filter((item) => [item.title, item.summary, item.destination, item.tags.join(' ')].join(' ').toLowerCase().includes(keyword))
    }
    return {
      list: list.map(enrichStrategy),
      total: list.length
    }
  })
}

export function getStrategyDetail(id) {
  return backendFirst({
    url: `/api/strategies/${id}`,
    method: 'GET'
  }, () => enrichStrategy(strategies.find((item) => String(item.id) === String(id))))
}

export function createStrategy(payload) {
  return backendFirst({
    url: '/api/strategies',
    method: 'POST',
    data: payload
  }, () => {
    const nextItem = {
      id: getNextStrategyId(),
      type: 'strategy',
      title: payload.title,
      summary: payload.summary,
      content: payload.content,
      destination: payload.destination,
      category: payload.category || '自然风光',
      days: Number(payload.days || 3),
      coverUrl: payload.coverUrl || 'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&q=80&w=2000',
      tags: payload.tags || ['AI生成', payload.destination].filter(Boolean),
      author: currentUser,
      likeCount: 0,
      favoriteCount: 0,
      viewCount: 0,
      createdAt: getNowLabel()
    }
    strategies.unshift(nextItem)
    currentUser.stats.posts += 1
    return enrichStrategy(nextItem)
  })
}

export function saveStrategyDraft(payload) {
  return backendFirst({
    url: '/api/strategies/drafts',
    method: 'POST',
    data: payload
  }, () => {
    const nextItem = {
      id: getNextDraftId(),
      draftType: 'strategy',
      title: payload.title || `${payload.destination || '未命名目的地'} 行程草稿`,
      updatedAt: getNowLabel(),
      payload: {
        ...payload
      }
    }
    drafts.unshift(nextItem)
    return nextItem
  })
}

export function toggleStrategyFavorite(id) {
  return backendFirst({
    url: `/api/strategies/${id}/favorite`,
    method: 'POST'
  }, () => {
    const item = strategies.find((entry) => String(entry.id) === String(id))
    const index = interactionState.favoritedStrategies.indexOf(item.id)
    let isFavorited = false
    if (index >= 0) {
      interactionState.favoritedStrategies.splice(index, 1)
      item.favoriteCount = Math.max(0, item.favoriteCount - 1)
    } else {
      interactionState.favoritedStrategies.push(item.id)
      item.favoriteCount += 1
      isFavorited = true
    }
    return {
      isFavorited,
      favoriteCount: item.favoriteCount
    }
  })
}

export function toggleStrategyLike(id) {
  return backendFirst({
    url: `/api/strategies/${id}/like`,
    method: 'POST'
  }, () => {
    const item = strategies.find((entry) => String(entry.id) === String(id))
    const index = interactionState.likedStrategies.indexOf(item.id)
    let isLiked = false
    if (index >= 0) {
      interactionState.likedStrategies.splice(index, 1)
      item.likeCount = Math.max(0, item.likeCount - 1)
    } else {
      interactionState.likedStrategies.push(item.id)
      item.likeCount += 1
      isLiked = true
    }
    return {
      isLiked,
      likeCount: item.likeCount
    }
  })
}

export function getStrategyComments(id) {
  return backendFirst({
    url: `/api/strategies/${id}/comments`,
    method: 'GET'
  }, () => ({
    list: interactionState.strategyComments[id] || []
  }))
}

export function createStrategyComment(id, payload) {
  return backendFirst({
    url: `/api/strategies/${id}/comments`,
    method: 'POST',
    data: payload
  }, () => {
    const nextItem = {
      id: Date.now(),
      userId: currentUser.id,
      nickname: currentUser.nickname,
      avatar: currentUser.avatar,
      content: payload.content,
      createdAt: '刚刚'
    }
    if (!interactionState.strategyComments[id]) {
      interactionState.strategyComments[id] = []
    }
    interactionState.strategyComments[id].unshift(nextItem)
    return nextItem
  })
}

export function shareStrategy(id) {
  return backendFirst({
    url: `/api/strategies/${id}/share`,
    method: 'POST'
  }, () => {
    interactionState.strategyShareCount[id] = (interactionState.strategyShareCount[id] || 0) + 1
    return {
      shareCount: interactionState.strategyShareCount[id]
    }
  })
}
