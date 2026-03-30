# 接入渠道配置

## 支持的渠道

| 渠道 | 状态 | 配置难度 |
|------|------|---------|
| 飞书 | ✅ 已配置 | 中等 |
| 企业微信 | ✅ 可用 | 中等 |
| 钉钉 | ✅ 可用 | 简单 |
| QQBot | ✅ 可用 | 简单 |
| 网页 | ✅ 内置 | 无需配置 |

## 飞书配置

### 1. 创建应用

1. 访问 https://open.feishu.cn/
2. 创建企业自建应用
3. 获取 App ID 和 App Secret

### 2. 配置权限

在应用权限管理中添加：
- `im:message`
- `im:message.group_at_msg`
- `im:chat`

### 3. 配置Webhook

在应用事件订阅中配置WebSocket模式

### 4. 填入配置

编辑 `configs/openclaw.json`:

```json
{
  "channels": {
    "feishu": {
      "appId": "YOUR_APP_ID",
      "appSecret": "YOUR_APP_SECRET"
    }
  }
}
```

## 企业微信配置

### 1. 创建应用

1. 企业微信管理后台
2. 创建自建应用
3. 获取 AgentId

### 2. 配置

编辑配置文件中 `channels.wecom` 部分

## 钉钉配置

### 1. 创建应用

1. 钉钉开放平台
2. 创建企业内部应用
3. 获取 AppKey 和 AppSecret

### 2. 配置

编辑配置文件中 `channels.ddingtalk` 部分
