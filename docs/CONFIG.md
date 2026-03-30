# 配置说明

## 配置文件位置

主配置文件：`~/.openclaw/openclaw.json`

## 需要配置的 Keys

| 配置项 | 说明 | 获取方式 |
|--------|------|---------|
| MiniMax API Key | LLM Provider | https://www.minimaxi.com/ |
| Feishu App ID/Secret | 飞书机器人 | https://open.feishu.cn/ |
| GitHub PAT | 代码同步 | https://github.com/settings/tokens |
| Notion API Key | 知识库 | https://www.notion.so/my-integrations |
| Brave API Key | 新闻搜索 | https://brave.com/search/api/ |

## Agent 配置

每个部门的 Agent 配置在 `configs/agents/` 目录下。

修改后需重启 Gateway 生效。
