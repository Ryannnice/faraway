# 静态图片目录说明

你可以把需要替换的本地图片放到这些目录里：

- `static/bg/`
  - 放 App 的背景图
  - 建议文件名：
    - `login-bg.jpg`
    - `home-hero.jpg`
    - `profile-cover.jpg`

- `static/cover/`
  - 放攻略 / Vlog 的默认封面图
  - 建议文件名：
    - `strategy-default.jpg`
    - `vlog-default.jpg`

- `static/avatar/`
  - 放本地默认头像或示例头像
  - 建议文件名：
    - `user-default.jpg`
    - `guest-1.jpg`
    - `guest-2.jpg`
    - `guest-3.jpg`

建议裁图比例：

- 背景图：`16:9` 或 `3:2`
- 封面图：`4:3`
- 头像：`1:1`

建议导出宽度：

- 背景图：`1440` 到 `1600`
- 封面图：`960` 到 `1200`
- 头像：`400` 到 `600`

图片准备好后，前端可以这样引用：

- `/static/bg/login-bg.jpg`
- `/static/bg/home-hero.jpg`
- `/static/bg/profile-cover.jpg`
- `/static/avatar/user-default.jpg`

补充说明：

- 目录里的 `.gitkeep` 只是用来保留空文件夹的占位文件。
- 你不用管它，也不用删它。
- 直接把图片放进对应目录就可以。
