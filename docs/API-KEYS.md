# API Keys 配置清单

## 必须配置的Keys

### MiniMax API Key

- **用途**: LLM大模型
- **获取**: https://www.minimaxi.com/
- **配置项**: `models.providers.minimax.apiKey`

### 飞书 App Credentials

- **用途**: 飞书机器人
- **获取**: https://open.feishu.cn/
- **配置项**: `channels.feishu.appId`, `channels.feishu.appSecret`

## 可选配置的Keys

### GitHub PAT

- **用途**: GitHub代码同步
- **获取**: https://github.com/settings/tokens
- **权限**: repo (全权限)
- **配置项**: 存储在 MEMORY.md

### Notion API Key

- **用途**: 知识库读写
- **获取**: https://www.notion.so/my-integrations
- **配置项**: 存储在各Agent的MEMORY.md

### Brave Search API Key

- **用途**: 新闻搜索
- **获取**: https://brave.com/search/api/
- **配置项**: 环境变量 BRAVE_SEARCH_API_KEY

## 配置步骤

1. 复制模板配置
```bash
cp configs/openclaw.json.example configs/openclaw.json
```

2. 替换占位符
```bash
# YOUR_KEY_HERE → 真实Key
sed -i 's/YOUR_KEY_HERE/real-key-value/g' configs/openclaw.json
```

3. 验证配置
```bash
openclaw gateway status
```
