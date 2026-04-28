import { backendFirst } from '../request'
import { currentUser, interactionState, vlogs } from '../mock-data'

function enrichPost(item) {
  if (!item) {
    return null
  }
  const commentList = interactionState.postComments[item.id] || []
  return {
    ...item,
    isLiked: interactionState.likedVlogs.includes(item.id),
    isFavorited: interactionState.favoritedVlogs.includes(item.id),
    commentCount: commentList.length,
    shareCount: interactionState.postShareCount[item.id] || 0
  }
}

export function getPostList(params = {}) {
  return backendFirst({
    url: '/api/posts',
    method: 'GET',
    data: params
  }, () => {
    let list = [...vlogs]
    if (params.keyword) {
      const keyword = params.keyword.toLowerCase()
      list = list.filter((item) => [item.title, item.location, item.tags.join(' '), item.content].join(' ').toLowerCase().includes(keyword))
    }
    return { list: list.map(enrichPost), total: list.length }
  })
}

export function getPostDetail(id) {
  return backendFirst({
    url: `/api/posts/${id}`,
    method: 'GET'
  }, () => enrichPost(vlogs.find((item) => String(item.id) === String(id))))
}

export function createPost(payload) {
  return backendFirst({
    url: '/api/posts',
    method: 'POST',
    data: payload
  }, () => ({
    id: Date.now(),
    author: currentUser,
    ...payload
  }))
}

export function createPostDraft(payload) {
  return backendFirst({
    url: '/api/posts/drafts',
    method: 'POST',
    data: payload
  }, () => ({
    id: Date.now(),
    draftType: 'post',
    ...payload
  }))
}

export function getMyPosts() {
  return backendFirst({
    url: '/api/my/posts',
    method: 'GET'
  }, () => ({
    list: vlogs.filter((item) => item.author.id === currentUser.id).map(enrichPost)
  }))
}

export function togglePostLike(id) {
  return backendFirst({
    url: `/api/posts/${id}/like`,
    method: 'POST'
  }, () => {
    const item = vlogs.find((entry) => String(entry.id) === String(id))
    const index = interactionState.likedVlogs.indexOf(item.id)
    let isLiked = false
    if (index >= 0) {
      interactionState.likedVlogs.splice(index, 1)
      item.likeCount = Math.max(0, item.likeCount - 1)
    } else {
      interactionState.likedVlogs.push(item.id)
      item.likeCount += 1
      isLiked = true
    }
    return {
      isLiked,
      likeCount: item.likeCount
    }
  })
}

export function togglePostFavorite(id) {
  return backendFirst({
    url: `/api/posts/${id}/favorite`,
    method: 'POST'
  }, () => {
    const item = vlogs.find((entry) => String(entry.id) === String(id))
    const index = interactionState.favoritedVlogs.indexOf(item.id)
    let isFavorited = false
    if (index >= 0) {
      interactionState.favoritedVlogs.splice(index, 1)
      item.favoriteCount = Math.max(0, item.favoriteCount - 1)
    } else {
      interactionState.favoritedVlogs.push(item.id)
      item.favoriteCount += 1
      isFavorited = true
    }
    return {
      isFavorited,
      favoriteCount: item.favoriteCount
    }
  })
}

export function getPostComments(id) {
  return backendFirst({
    url: `/api/posts/${id}/comments`,
    method: 'GET'
  }, () => ({
    list: interactionState.postComments[id] || []
  }))
}

export function createPostComment(id, payload) {
  return backendFirst({
    url: `/api/posts/${id}/comments`,
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
    if (!interactionState.postComments[id]) {
      interactionState.postComments[id] = []
    }
    interactionState.postComments[id].unshift(nextItem)
    return nextItem
  })
}

export function sharePost(id) {
  return backendFirst({
    url: `/api/posts/${id}/share`,
    method: 'POST'
  }, () => {
    interactionState.postShareCount[id] = (interactionState.postShareCount[id] || 0) + 1
    return {
      shareCount: interactionState.postShareCount[id]
    }
  })
}
