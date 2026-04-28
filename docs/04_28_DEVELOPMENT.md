# FarawayBackend 开发说明

## 1. 当前后端结构

- Web：FastAPI
- 数据：SQLite
- 文件：阿里云 OSS
- AI：阿里云百炼
- 鉴权：JWT

## 2. 用户隔离设计

这次已经从“伪登录”改成了“真实账号体系”。

### 2.1 账号数据

现在分成三类数据：

1. `auth_accounts`
2. `auth_identities`
3. `users`

含义：

- `auth_accounts`：账号主表，存用户名、手机号、密码哈希、登录方式
- `auth_identities`：登录索引，解决用户名 / 手机号查 UID
- `users`：公开用户资料，存昵称、头像、简介等

### 2.2 为什么这么拆

因为“认证信息”和“公开资料”不是一回事。

如果把密码哈希也塞到 `users`，后面做公开用户主页时容易混淆边界。现在拆开以后：

- 登录校验只看 `auth_accounts`
- 个人资料页只读 `users`

边界更清楚。

### 2.3 用户隔离如何落地

现在业务接口统一依赖 `Authorization: Bearer <token>`。

token 解出来是 `uid`，后端用这个 `uid` 做隔离：

- 我的草稿只能我自己看
- 我的发布按当前用户过滤
- 我的招募、我的申请记录按当前用户过滤
- 点赞、收藏、评论都按当前用户记录

## 3. 注册与登录流程

### 3.1 注册

`POST /api/auth/register`

流程：

1. 校验用户名格式
2. 校验密码长度
3. 检查用户名是否重复
4. 如果传了手机号，校验短信验证码
5. 创建 `auth_accounts`
6. 创建 `auth_identities`
7. 创建 `users`

### 3.2 密码登录

`POST /api/auth/password-login`

流程：

1. 根据用户名查 `auth_identities`
2. 找到 UID
3. 读 `auth_accounts`
4. 校验 PBKDF2 密码哈希
5. 生成 JWT

### 3.3 手机登录

`POST /api/auth/phone-login`

流程：

1. 校验短信验证码
2. 用手机号查 `auth_identities`
3. 找到账号
4. 生成 JWT

## 4. 安全策略

### 4.1 当前默认值

`.env` 默认已经改成：

```env
DEV_ALLOW_ANON_AUTH=false
DEV_TRUST_X_USER_HEADERS=false
```

这意味着：

- 不再允许匿名直接访问需要登录的接口
- 不再允许随便传 `X-User-Id` 冒充别人

### 4.2 密码存储

密码不是明文保存。

当前实现：

- `PBKDF2-HMAC-SHA256`
- 独立随机 salt
- 迭代次数来自 `PASSWORD_HASH_ITERATIONS`

## 5. SQLite 说明

当前仍然使用轻量文档式存储：

- 表固定为 `documents`
- `collection + id` 作为主键
- 业务内容存 JSON

优点：

- 开发快
- 字段变化快

缺点：

- 复杂查询差
- 数据量上来后不适合长期使用

如果后面正式上线并且用户量起来，建议迁移到 MySQL 或 PostgreSQL。

## 6. 现在适合继续做的事

下一步建议优先级：

1. 前端接入注册页和登录页
2. 前端请求统一带 Bearer token
3. 把微信登录正式联通
4. 给用户补修改密码 / 重置密码
5. 给短信接口接真实短信服务
