import { backendFirst } from '../request'
import { currentUser, guestUsers, interactionState, strategies, vlogs } from '../mock-data'

function getAllUsers() {
  return [currentUser, ...guestUsers]
}

function findUser(userId) {
  return getAllUsers().find((item) => Number(item.id) === Number(userId)) || guestUsers[0]
}

function getFavoriteContents() {
  const strategyItems = strategies.filter((item) => interactionState.favoritedStrategies.includes(item.id)).map((item) => ({ ...item, contentType: 'strategy' }))
  const vlogItems = vlogs.filter((item) => interactionState.favoritedVlogs.includes(item.id)).map((item) => ({ ...item, contentType: 'vlog' }))
  return [...strategyItems, ...vlogItems]
}

function getLikeContents() {
  const strategyItems = strategies.filter((item) => interactionState.likedStrategies.includes(item.id)).map((item) => ({ ...item, contentType: 'strategy' }))
  const vlogItems = vlogs.filter((item) => interactionState.likedVlogs.includes(item.id)).map((item) => ({ ...item, contentType: 'vlog' }))
  return [...strategyItems, ...vlogItems]
}

export function getUserProfile() {
  return backendFirst({
    url: '/api/user/profile',
    method: 'GET'
  }, () => currentUser)
}

export function updateUserProfile(payload) {
  return backendFirst({
    url: '/api/user/profile',
    method: 'PUT',
    data: payload
  }, () => ({
    ...currentUser,
    ...payload
  }))
}

export function getMyStats() {
  return backendFirst({
    url: '/api/user/stats',
    method: 'GET'
  }, () => ({
    postCount: currentUser.stats.posts,
    strategyCount: strategies.filter((item) => item.author.id === currentUser.id).length,
    favoriteCount: getFavoriteContents().length,
    likeCount: getLikeContents().length
  }))
}

export function getUserPublicProfile(userId) {
  return backendFirst({
    url: `/api/users/${userId}`,
    method: 'GET'
  }, () => {
    const user = findUser(userId)
    const posts = [...strategies.filter((item) => item.author.id === user.id), ...vlogs.filter((item) => item.author.id === user.id)]
    return {
      ...user,
      stats: {
        posts: posts.length,
        favorites: posts.reduce((sum, item) => sum + Number(item.favoriteCount || 0), 0),
        likes: posts.reduce((sum, item) => sum + Number(item.likeCount || 0), 0)
      },
      posts
    }
  })
}

export function getUserPublishedContent(userId) {
  return backendFirst({
    url: `/api/users/${userId}/contents`,
    method: 'GET'
  }, () => ({
    list: [...strategies.filter((item) => item.author.id === Number(userId)), ...vlogs.filter((item) => item.author.id === Number(userId))]
  }))
}

export function getMyFavoriteContents() {
  return backendFirst({
    url: '/api/my/favorites',
    method: 'GET'
  }, () => ({
    list: getFavoriteContents()
  }))
}

export function getMyLikeContents() {
  return backendFirst({
    url: '/api/my/likes',
    method: 'GET'
  }, () => ({
    list: getLikeContents()
  }))
}

export function getMyDrafts() {
  return backendFirst({
    url: '/api/my/drafts',
    method: 'GET'
  }, () => ({
    list: []
  }))
}

export function getMyNotifications() {
  return backendFirst({
    url: '/api/my/notifications',
    method: 'GET'
  }, () => ({
    list: []
  }))
}
