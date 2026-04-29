# FARAWAY P0

按 `04_29_完整重构找搭子.md` 落地的新单仓库 P0 项目。

## 目录

```text
FARAWAY/
├── apps/
│   ├── api/
│   └── mobile/
├── docs/
├── infra/
└── scripts/
```

## apps/api

- 技术栈：`FastAPI + SQLAlchemy 2.x + Pydantic v2 + Alembic`
- 已实现模块：
  - 认证：注册、密码登录、登出
  - 用户：当前资料读取/更新、他人主页
  - AI：攻略生成、见面地点生成回退
  - 匹配：实时请求、候选、同意/拒绝、备注、惰性状态推进
  - 通知：只读列表
  - 上传：头像图片上传
- 自动化测试：

```bash
cd apps/api
PYTHONPATH=. ../../.venv/bin/pytest tests -q
```

## apps/mobile

- 技术栈：`Uni-app + Vue 3 + TypeScript + Pinia + SCSS`
- P0 页面：
  - 登录页
  - 首页
  - AI 攻略页
  - 找搭子页
  - 我的搭子页
  - 通知页
  - 个人资料页
  - 他人主页页
  - 设置页

## 本地运行建议

1. 启动 PostgreSQL：

```bash
docker compose -f infra/docker-compose.yml up -d
```

2. 准备后端环境变量：

```bash
cp apps/api/.env.example apps/api/.env
```

3. 启动 API：

```bash
cd apps/api
PYTHONPATH=. ../../.venv/bin/uvicorn app.main:app --reload
```

4. 在 Uni-app 工具链中打开 `apps/mobile/`。

## 当前验证结果

- 后端接口测试：`7 passed`
- 前端：已完成源码落地，当前未在本机安装 Uni-app 工具链进行编译验证
