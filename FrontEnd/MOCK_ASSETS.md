# Mock Assets Guide

如果你要让 `client_rebuild/` 在没有后端的情况下更接近真实效果，主要需要补两类资源：

## 1. 图片链接放哪里

### 攻略封面图

文件：

- `client_rebuild/api/mock-data.js`

字段：

- `strategies[].coverUrl`

### Vlog 封面图

文件：

- `client_rebuild/api/mock-data.js`

字段：

- `vlogs[].coverUrl`

### 用户头像

文件：

- `client_rebuild/api/mock-data.js`

字段：

- `currentUser.avatar`
- `guestUsers[].avatar`
- `vlogs[].author.avatar`
- `strategies[].author.avatar`

## 2. 视频链接放哪里

文件：

- `client_rebuild/api/mock-data.js`

字段：

- `vlogs[].mediaList[0].url`

说明：

- 当前前端默认每条 Vlog 先只读取 `mediaList` 的第一条视频
- 最稳妥的是先统一使用 `.mp4` 直链

## 3. 推荐的免费图片/视频素材站

图片：

- Unsplash
- Pexels Photos
- Pixabay Images

视频：

- Pexels Videos
- Pixabay Videos
- Mixkit
- Coverr

## 4. 第一版最少要补哪些资源

如果你只是想“先看效果”，最少准备这些：

- 8 到 12 张攻略封面图
- 6 到 10 张 Vlog 封面图
- 6 条可直链播放的 MP4 视频
- 4 到 8 个用户头像

## 5. 建议的素材风格

为了和 `faraway/` 风格接近，建议优先找这些类型：

- 冷色调风景
- 大地形、雪山、海岸线、城市夜景
- 高反差、低饱和、带空气感
- 纵向视频封面优先

## 6. 不建议

- 不建议第一版就混入很多来源不明的短视频链接
- 不建议使用需要复杂鉴权或防盗链的视频 URL
- 不建议同时混用太多尺寸比例，容易让卡片流观感变差
