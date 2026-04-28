const VIDEO_URL_PATTERN = /\.(mp4|mov|m4v|webm|ogg|m3u8)(\?.*)?$/i

export function getPostVideoUrl(item) {
  if (!item || !Array.isArray(item.mediaList)) {
    return ''
  }
  const videoItem = item.mediaList.find((entry) => entry && entry.type === 'video' && entry.url)
  return videoItem ? videoItem.url : ''
}

export function hasPostVideo(item) {
  return !!getPostVideoUrl(item)
}

export function isVideoLikeUrl(url) {
  return !!(url && VIDEO_URL_PATTERN.test(url))
}

export function getPostPosterUrl(item) {
  const coverUrl = item && item.coverUrl ? item.coverUrl : ''
  const videoUrl = getPostVideoUrl(item)
  if (!coverUrl || coverUrl === videoUrl || isVideoLikeUrl(coverUrl)) {
    return ''
  }
  return coverUrl
}
