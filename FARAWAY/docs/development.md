# Development Notes

## Backend

- 默认使用本地 SQLite URL 便于快速起步；`.env.example` 提供 PostgreSQL 配置样例。
- 测试验证路径是 `apps/api/tests/`。
- `alembic/versions/20260429_0001_p0_schema.py` 是初始 schema 迁移。

## Frontend

- `api/` 统一封装请求。
- `stores/` 持有跨页登录态、资料、匹配态、通知态。
- 所有页面都采用 `script setup`。
- 非首页页面统一使用 `components/AppNavBar.vue`。
