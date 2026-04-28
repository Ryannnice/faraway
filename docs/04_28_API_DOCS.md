# Faraway 前端认证接口文档

本文档只包含前端当前需要接入的注册、登录、登录态相关接口。

统一响应格式：

```json
{
  "code": 0,
  "message": "ok",
  "data": {}
}
```

## 1. 当前认证规则

当前前端流程按下面执行：

1. 用户注册
2. 用户登录
3. 前端保存 `token`
4. 后续请求在请求头带上：

```http
Authorization: Bearer <token>
```

当前版本下：

- 注册只需要：`username` + `password`
- 不要求绑定手机号
- 不要求短信验证码
- 不允许匿名访问需要登录的接口

---

## 2. 注册

### 接口

`POST /api/auth/register`

### 请求体

前端当前只需要传这两个字段：

```json
{
  "username": "alice_01",
  "password": "pass123456"
}
```

如果你以后想补昵称，也可以多传：

```json
{
  "username": "alice_01",
  "password": "pass123456",
  "nickname": "Alice"
}
```

### 字段说明

- `username`：必填，3-32 位，只允许字母、数字、下划线
- `password`：必填，6-128 位
- `nickname`：可选

### 成功返回示例

```json
{
  "code": 0,
  "message": "registered",
  "data": {
    "id": "d07bcbf0cffb4e338a1541fb10c7a057",
    "username": "alice_01",
    "phone": "",
    "nickname": "Alice",
    "avatar": "",
    "createdAt": "2026-04-27T11:00:00+00:00"
  }
}
```

### 失败场景

- 用户名已存在：`409`
- 用户名格式不合法：`400`
- 密码长度不合法：`400`

---

## 3. 账号密码登录

### 接口

`POST /api/auth/password-login`

### 请求体

```json
{
  "username": "alice_01",
  "password": "pass123456"
}
```

### 成功返回示例

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "token": "jwt_token_value",
    "refreshToken": "refresh_token_value",
    "loginType": "password",
    "userInfo": {
      "id": "d07bcbf0cffb4e338a1541fb10c7a057",
      "nickname": "Alice",
      "avatar": ""
    }
  }
}
```

### 前端处理

登录成功后前端至少要缓存：

- `token`
- `userInfo`

后续所有需要登录的接口都带：

```http
Authorization: Bearer <token>
```

### 失败场景

- 用户名或密码错误：`401`
- 账号被禁用：`403`

---

## 4. 退出登录

### 接口

`POST /api/auth/logout`

### 请求头

```http
Authorization: Bearer <token>
```

### 成功返回示例

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "userId": "d07bcbf0cffb4e338a1541fb10c7a057"
  }
}
```

### 前端处理

退出成功后前端清空本地：

- `token`
- `refreshToken`
- `userInfo`

---

## 5. 获取当前用户资料

### 接口

`GET /api/user/profile`

### 请求头

```http
Authorization: Bearer <token>
```

### 成功返回示例

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "id": "d07bcbf0cffb4e338a1541fb10c7a057",
    "nickname": "Alice",
    "avatar": "",
    "bio": "",
    "gender": "unknown",
    "createdAt": "2026-04-27T11:00:00+00:00",
    "updatedAt": "2026-04-27T11:00:00+00:00"
  }
}
```

---

## 6. 更新当前用户资料

### 接口

`PUT /api/user/profile`

### 请求头

```http
Authorization: Bearer <token>
```

### 请求体

```json
{
  "nickname": "Alice New",
  "bio": "探索未知的旅人",
  "avatar": "https://example.com/avatar.jpg"
}
```

### 成功返回示例

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "id": "d07bcbf0cffb4e338a1541fb10c7a057",
    "nickname": "Alice New",
    "avatar": "https://example.com/avatar.jpg",
    "bio": "探索未知的旅人",
    "gender": "unknown",
    "createdAt": "2026-04-27T11:00:00+00:00",
    "updatedAt": "2026-04-27T11:30:00+00:00"
  }
}
```

---

## 7. 前端最小接入流程

### 注册页

调用：

`POST /api/auth/register`

请求体：

```json
{
  "username": "alice_01",
  "password": "pass123456"
}
```

### 登录页

调用：

`POST /api/auth/password-login`

请求体：

```json
{
  "username": "alice_01",
  "password": "pass123456"
}
```

### 登录成功后

前端保存 `token`，并在后续请求统一加：

```http
Authorization: Bearer <token>
```

---

## 8. 当前不需要前端接的接口

下面两个接口后端还保留着，但你现在这版前端注册流程不需要接：

- `POST /api/auth/send-sms-code`
- `POST /api/auth/phone-login`

它们可以先忽略。
