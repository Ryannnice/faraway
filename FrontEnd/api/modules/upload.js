import { getToken } from '../../utils/storage'
import { buildUrl } from '../request'

function uploadMedia(file, url) {
  const filePath = file?.path || file?.tempFilePath
  if (!filePath) {
    return Promise.reject(new Error('No file selected'))
  }

  const token = getToken()

  return new Promise((resolve, reject) => {
    uni.uploadFile({
      url: buildUrl(url),
      filePath,
      name: 'file',
      header: token ? { Authorization: `Bearer ${token}` } : {},
      success: (response) => {
        const statusCode = response.statusCode || 0
        if (statusCode < 200 || statusCode >= 300) {
          reject(response)
          return
        }

        try {
          const body = typeof response.data === 'string' ? JSON.parse(response.data) : response.data
          if (body && typeof body === 'object' && Object.prototype.hasOwnProperty.call(body, 'code')) {
            if (body.code !== 0) {
              reject(body)
              return
            }
            resolve(body.data || {})
            return
          }
          resolve(body || {})
        } catch (error) {
          reject(error)
        }
      },
      fail: reject
    })
  })
}

export function uploadImage(file) {
  return uploadMedia(file, '/api/upload/image')
}

export function uploadVideo(file) {
  return uploadMedia(file, '/api/upload/video')
}
