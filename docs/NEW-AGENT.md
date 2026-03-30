# 新增 Agent 指南

## 添加新Agent步骤

### 1. 创建Agent配置

在 `configs/openclaw.json` 的 `agents.list` 中添加：

```json
{
  "id": "new-agent-id",
  "workspace": "~/.openclaw/workspaces/yunshang-taihe/new-agent",
  "subagents": {
    "allowAgents": []
  }
}
```

### 2. 创建工作区目录

```bash
mkdir -p ~/.openclaw/workspaces/yunshang-taihe/new-agent
```

### 3. 配置Agent角色

创建 `~/.openclaw/workspaces/yunshang-taihe/new-agent/SOUL.md`:

```markdown
# Agent角色定义

你是[角色名称]，负责[职责描述]。

## 核心职责
- ...
```

### 4. 安装Skills

```bash
openclaw skills install <skill-name>
```

### 5. 重启Gateway

```bash
openclaw gateway restart
```

## 示例：新增"客服部"

1. 在 `agents.list` 添加客服部Agent
2. 创建工作区目录
3. 配置SOUL.md
4. 安装客服相关Skills
5. 重启Gateway
