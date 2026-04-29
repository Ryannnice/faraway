<template>
  <view class="note-page">
    <AppHeader title="创作中心" subtitle="Upload" fallback="/pages/profile/index" />

    <view class="type-row">
      <view class="type-pill" :class="{ active: form.type === 'strategy' }" @tap="switchType('strategy')">图文笔记</view>
      <view class="type-pill" :class="{ active: form.type === 'vlog' }" @tap="switchType('vlog')">视频 Vlog</view>
    </view>

    <template v-if="form.type === 'strategy'">
      <scroll-view class="media-scroll" scroll-x enable-flex show-scrollbar="false">
        <view class="media-row">
          <view v-for="(item, index) in form.imageList" :key="item.id" class="media-card">
            <image class="media-preview" :src="item.previewUrl || item.remoteUrl" mode="aspectFill" />
            <view class="media-overlay">
              <text class="media-index">{{ index + 1 }}</text>
              <text v-if="item.status === 'uploading'" class="media-state">上传中</text>
              <text v-else-if="item.status === 'error'" class="media-state error">失败</text>
            </view>
            <view class="media-remove" @tap.stop="removeImage(index)">×</view>
          </view>

          <view v-if="canAddMoreImages" class="add-card" @tap="chooseImages">
            <text class="add-icon">+</text>
            <text class="add-text">{{ form.imageList.length ? '继续加图' : '添加图片' }}</text>
          </view>
        </view>
      </scroll-view>
    </template>

    <view v-else class="video-box glass-card">
      <video
        v-if="displayVideoUrl"
        class="video-preview"
        :src="displayVideoUrl"
        :poster="displayVideoPoster"
        object-fit="cover"
        controls
      />
      <view v-else class="video-empty" @tap="chooseVideoMedia">
        <text class="add-icon">+</text>
        <text class="add-text">上传视频</text>
      </view>
      <view v-if="displayVideoUrl" class="video-actions">
        <text class="video-action" @tap="chooseVideoMedia">重新选择</text>
      </view>
      <text v-if="uploadingVideo" class="video-status">视频上传中...</text>
    </view>

    <view class="editor-section">
      <input v-model="form.title" class="title-input" placeholder="添加标题" placeholder-style="color: rgba(246,240,232,0.22)" />
      <textarea v-model="form.content" class="content-input" placeholder="展开说说，分享你的见地与心情..." placeholder-style="color: rgba(246,240,232,0.18)" />
    </view>

    <view class="chip-row">
      <text class="chip">#旅途记录</text>
      <text class="chip">#灵感瞬间</text>
      <text class="chip">#Faraway</text>
    </view>

    <view class="field-list">
      <view class="field-row glass-card">
        <text class="field-name">标记地点</text>
        <input v-model="form.location" class="field-value" placeholder="添加地点..." placeholder-style="color: rgba(246,240,232,0.22)" />
      </view>
      <view class="field-row glass-card">
        <text class="field-name">公开可见</text>
        <text class="field-hint">默认公开</text>
      </view>
      <view class="field-row glass-card">
        <text class="field-name">高级选项</text>
        <text class="field-hint">后续补充</text>
      </view>
    </view>

    <view class="action-row">
      <view class="draft-btn" @tap="saveDraft">存草稿</view>
      <view class="publish-btn" @tap="publish">{{ form.type === 'strategy' ? '发布笔记' : '发布视频' }}</view>
    </view>
  </view>
</template>

<script>
import AppHeader from '../../components/common/AppHeader.vue'
import { createPost, createPostDraft } from '../../api/modules/post'
import { createStrategy, saveStrategyDraft } from '../../api/modules/strategy'
import { uploadImage, uploadVideo } from '../../services/upload'
import { clearPendingDraft, getPendingDraft } from '../../utils/storage'
import { go } from '../../utils/navigation'

function createImageItem(localPath) {
  return {
    id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
    previewUrl: localPath,
    remoteUrl: '',
    status: 'uploading'
  }
}

export default {
  components: {
    AppHeader
  },
  data() {
    return {
      form: {
        type: 'strategy',
        title: '',
        location: '',
        content: '',
        coverUrl: '',
        mediaList: [],
        imageList: []
      },
      uploadingVideo: false,
      videoPreviewUrl: '',
      remoteVideoUrl: '',
      videoPosterPreviewUrl: ''
    }
  },
  computed: {
    canAddMoreImages() {
      return this.form.imageList.length < 9
    },
    displayVideoUrl() {
      return this.videoPreviewUrl || this.remoteVideoUrl
    },
    displayVideoPoster() {
      return this.videoPosterPreviewUrl || this.form.coverUrl
    },
    hasUploadingImages() {
      return this.form.imageList.some((item) => item.status === 'uploading')
    }
  },
  onLoad(options) {
    if (options && options.draft) {
      this.restoreDraft()
    }
  },
  methods: {
    switchType(type) {
      this.form.type = type
    },
    restoreDraft() {
      const draft = getPendingDraft()
      if (!draft || !draft.payload) {
        return
      }
      this.form = {
        ...this.form,
        ...draft.payload,
        imageList: Array.isArray(draft.payload.imageList) ? draft.payload.imageList : [],
        type: draft.draftType === 'strategy' ? 'strategy' : 'vlog'
      }
      this.videoPreviewUrl = ''
      this.videoPosterPreviewUrl = ''
      this.remoteVideoUrl =
        draft.payload && Array.isArray(draft.payload.mediaList) && draft.payload.mediaList[0]
          ? draft.payload.mediaList[0].url || ''
          : ''
      clearPendingDraft()
    },
    syncStrategyCover() {
      const firstUploaded = this.form.imageList.find((item) => item.remoteUrl)
      this.form.coverUrl = firstUploaded ? firstUploaded.remoteUrl : ''
    },
    serializeStrategyImages() {
      return this.form.imageList
        .filter((item) => item && item.remoteUrl)
        .map((item) => ({
          url: item.remoteUrl
        }))
    },
    buildStrategyPayload() {
      const uploadedImages = this.serializeStrategyImages()
      return {
        title: this.form.title,
        summary: this.form.content ? this.form.content.slice(0, 48) : '',
        content: this.form.content,
        destination: this.form.location,
        days: 3,
        coverUrl: uploadedImages.length ? uploadedImages[0].url : '',
        imageList: uploadedImages,
        tags: this.form.location ? [this.form.location] : []
      }
    },
    buildPostPayload(status = 'published') {
      return {
        type: 'vlog',
        title: this.form.title,
        location: this.form.location,
        content: this.form.content,
        coverUrl: this.form.coverUrl,
        mediaList: this.form.mediaList,
        tags: this.form.location ? [this.form.location] : [],
        status
      }
    },
    chooseImages() {
      if (!this.canAddMoreImages) {
        uni.showToast({
          title: '最多添加 9 张图片',
          icon: 'none'
        })
        return
      }
      uni.chooseImage({
        count: 9 - this.form.imageList.length,
        success: (result) => {
          const tempFiles = Array.isArray(result.tempFiles) ? result.tempFiles : []
          tempFiles.forEach((file) => {
            const localPath = file && (file.path || file.tempFilePath)
            if (!localPath) {
              return
            }
            const imageItem = createImageItem(localPath)
            this.form.imageList.push(imageItem)
            this.uploadSingleImage(file, imageItem.id)
          })
        }
      })
    },
    async uploadSingleImage(file, imageId) {
      try {
        const uploaded = await uploadImage(file)
        const target = this.form.imageList.find((item) => item.id === imageId)
        if (!target) {
          return
        }
        target.remoteUrl = uploaded.url || ''
        target.status = 'done'
        this.syncStrategyCover()
      } catch (error) {
        const target = this.form.imageList.find((item) => item.id === imageId)
        if (target) {
          target.status = 'error'
        }
        uni.showToast({
          title: error && error.message ? error.message : '图片上传失败',
          icon: 'none'
        })
      }
    },
    removeImage(index) {
      this.form.imageList.splice(index, 1)
      this.syncStrategyCover()
    },
    chooseVideoMedia() {
      uni.chooseVideo({
        sourceType: ['album', 'camera'],
        compressed: false,
        success: async (result) => {
          this.videoPreviewUrl = result.tempFilePath || ''
          this.videoPosterPreviewUrl = result.thumbTempFilePath || ''
          this.remoteVideoUrl = ''
          this.uploadingVideo = true
          try {
            const uploaded = await uploadVideo({
              path: result.tempFilePath
            })
            let remoteCoverUrl = uploaded.coverUrl || ''
            if (!remoteCoverUrl && result.thumbTempFilePath) {
              try {
                const uploadedPoster = await uploadImage({
                  path: result.thumbTempFilePath
                })
                remoteCoverUrl = uploadedPoster.url || ''
              } catch (posterError) {
                console.warn('video poster upload failed', posterError)
              }
            }
            this.form.coverUrl = remoteCoverUrl
            this.remoteVideoUrl = uploaded.url || ''
            this.form.mediaList = this.remoteVideoUrl ? [{ type: 'video', url: this.remoteVideoUrl }] : []
            uni.showToast({
              title: '视频已上传',
              icon: 'none'
            })
          } catch (error) {
            this.videoPreviewUrl = ''
            this.videoPosterPreviewUrl = ''
            this.remoteVideoUrl = ''
            this.form.coverUrl = ''
            uni.showToast({
              title: error && error.message ? error.message : '视频上传失败',
              icon: 'none'
            })
          } finally {
            this.uploadingVideo = false
          }
        }
      })
    },
    async saveDraft() {
      if (this.form.type === 'strategy') {
        await saveStrategyDraft({
          ...this.buildStrategyPayload(),
          imageList: this.form.imageList
        })
      } else {
        await createPostDraft(this.buildPostPayload('draft'))
      }
      uni.showToast({
        title: '草稿已保存',
        icon: 'none'
      })
      go('/pages/drafts/index')
    },
    async publish() {
      if (this.form.type === 'strategy') {
        if (!this.form.imageList.length) {
          uni.showToast({
            title: '请先添加图片',
            icon: 'none'
          })
          return
        }
        if (this.hasUploadingImages) {
          uni.showToast({
            title: '图片上传中，请稍候',
            icon: 'none'
          })
          return
        }
        const result = await createStrategy(this.buildStrategyPayload())
        uni.redirectTo({
          url: `/pages/strategy-detail/index?id=${result.id}&fromPublish=1`
        })
        return
      }
      if (this.uploadingVideo) {
        uni.showToast({
          title: '视频上传中，请稍候',
          icon: 'none'
        })
        return
      }
      const result = await createPost(this.buildPostPayload())
      uni.redirectTo({
        url: `/pages/vlog-detail/index?id=${result.id}&fromPublish=1`
      })
    }
  }
}
</script>

<style scoped lang="scss">
.note-page {
  min-height: 100vh;
  padding: 24rpx 32rpx 56rpx;
  background: #19181f;
  color: #f6f0e8;
}

.type-row {
  display: flex;
  gap: 18rpx;
  margin-top: 14rpx;
}

.type-pill {
  flex: 1;
  height: 88rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.06);
  color: rgba(246, 240, 232, 0.62);
  font-size: 30rpx;
  font-weight: 600;
}

.type-pill.active {
  background: #ecd6b3;
  color: #10131c;
}

.media-scroll {
  margin-top: 30rpx;
  white-space: nowrap;
}

.media-row {
  display: flex;
  gap: 18rpx;
}

.media-card,
.add-card {
  position: relative;
  width: 180rpx;
  height: 220rpx;
  border-radius: 28rpx;
  overflow: hidden;
  flex-shrink: 0;
}

.media-card {
  background: #23232c;
}

.media-preview {
  width: 100%;
  height: 100%;
}

.media-overlay {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  padding: 14rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.media-index,
.media-state {
  padding: 6rpx 14rpx;
  border-radius: 999rpx;
  font-size: 20rpx;
  background: rgba(0, 0, 0, 0.42);
}

.media-state.error {
  color: #ff9582;
}

.media-remove {
  position: absolute;
  right: 12rpx;
  bottom: 12rpx;
  width: 44rpx;
  height: 44rpx;
  border-radius: 999rpx;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30rpx;
}

.add-card {
  border: 1rpx solid rgba(255, 255, 255, 0.06);
  background: #23232c;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.add-icon {
  font-size: 54rpx;
  line-height: 1;
  color: rgba(246, 240, 232, 0.62);
}

.add-text {
  margin-top: 12rpx;
  font-size: 24rpx;
  color: rgba(246, 240, 232, 0.4);
}

.video-box {
  position: relative;
  margin-top: 30rpx;
  height: 360rpx;
  border-radius: 34rpx;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.video-preview {
  width: 100%;
  height: 100%;
}

.video-actions {
  position: absolute;
  right: 22rpx;
  top: 22rpx;
}

.video-action {
  padding: 10rpx 18rpx;
  border-radius: 999rpx;
  background: rgba(0, 0, 0, 0.48);
  color: #fff;
  font-size: 22rpx;
}

.video-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.video-status {
  position: absolute;
  left: 24rpx;
  bottom: 24rpx;
  padding: 10rpx 18rpx;
  border-radius: 999rpx;
  background: rgba(0, 0, 0, 0.45);
  font-size: 22rpx;
}

.editor-section {
  margin-top: 34rpx;
}

.title-input {
  width: 100%;
  min-height: 70rpx;
  font-size: 54rpx;
  font-weight: 700;
  color: #f6f0e8;
}

.content-input {
  width: 100%;
  min-height: 320rpx;
  margin-top: 24rpx;
  font-size: 34rpx;
  line-height: 1.7;
  color: #f6f0e8;
}

.chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
  margin-top: 16rpx;
}

.chip {
  padding: 14rpx 22rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.06);
  font-size: 24rpx;
  color: rgba(246, 240, 232, 0.68);
}

.field-list {
  margin-top: 26rpx;
  display: flex;
  flex-direction: column;
  gap: 18rpx;
}

.field-row {
  min-height: 104rpx;
  padding: 0 28rpx;
  border-radius: 28rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.field-name {
  font-size: 30rpx;
  color: #f6f0e8;
}

.field-value,
.field-hint {
  text-align: right;
  font-size: 26rpx;
  color: rgba(246, 240, 232, 0.48);
}

.action-row {
  display: flex;
  gap: 22rpx;
  margin-top: 34rpx;
  position: sticky;
  bottom: 24rpx;
  z-index: 3;
}

.draft-btn,
.publish-btn {
  flex: 1;
  height: 96rpx;
  border-radius: 999rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 34rpx;
  font-weight: 700;
}

.draft-btn {
  border: 1rpx solid rgba(255, 255, 255, 0.12);
  color: rgba(246, 240, 232, 0.88);
}

.publish-btn {
  background: linear-gradient(135deg, #79c3ff 0%, #5aa8ff 52%, #3f86ff 100%);
  color: #ffffff;
}
</style>
