# Faraway

Faraway 的单仓库工作区，包含前端、后端和产品/接口文档。

## 目录结构

```text
faraway/
├─ BackEnd/   FastAPI 后端
├─ FrontEnd/  Uni-app 前端
└─ docs/      产品说明、开发文档、接口文档
```

## 子项目说明

- `BackEnd/`：认证、内容、找搭子、AI 攻略、上传接口
- `FrontEnd/`：Uni-app 客户端工程，适合用 HBuilderX 打开运行
- `docs/`：当前仓库共用文档，避免继续散落在前后端目录里

## 本地运行

### 后端

```bash
cd BackEnd
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

启动后访问：

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/health`

### 前端

1. 用 HBuilderX 打开 `FrontEnd/`
2. 按运行目标调整 `FrontEnd/api/config.js` 里的 `API_BASE_URL`
3. 运行到浏览器、模拟器或真机

联调建议：

- H5 本机联调：`http://127.0.0.1:8000`
- 手机或模拟器联调：改成你电脑的局域网 IP，例如 `http://192.168.1.20:8000`

## 文档位置

- `docs/04_28_API_DOCS.md`
- `docs/04_28_DEVELOPMENT.md`
- `docs/04_28_开发文档.md`
- `docs/04_28_接口文档.md`
- `docs/04_28_找搭子.md`
- `docs/04_29_找搭子功能说明.md`

## Git

当前目录已经按单仓库结构整理。你后续只需要在仓库根目录执行 Git 操作并推送到自己的账号。
