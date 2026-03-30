# 云上泰和 · OpenClaw 企业 Agent 系统

> 基于 OpenClaw 的多 Agent 企业数字化运营系统，仿"三省六部"架构

## 功能特点

- **多 Agent 协作**：10 个业务部门 × 4 Agent（一大三小），共 40 个 Agent
- **Skills 体系**：每个 Agent 可配置独立 Skills，支持按需增减
- **Channels**：支持飞书、企业微信、钉钉、QQBot 等多种接入方式
- **管理界面**：可视化 Agent 状态监控、Skills 管理、操作日志

## 快速开始

### 前置要求

- Node.js >= 18
- npm 或 pnpm
- Git

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/Echo-Kang98/openclaw-yunshang-taihe.git
cd openclaw-yunshang-taihe

# 2. 运行安装脚本
bash install.sh

# 3. 配置 API Keys
# 编辑 configs/openclaw.json，替换 YOUR_KEY_HERE 为真实密钥

# 4. 启动 Gateway
openclaw gateway start
```

### 配置说明

详见 [CONFIG.md](docs/CONFIG.md)

## 项目结构

```
openclaw-yunshang-taihe/
├── configs/          # Agent 配置文件
│   └── openclaw.json  # 主配置（API Keys 请自行替换）
├── skills/            # 通用 Skills
│   ├── self-improving/
│   ├── summarize/
│   └── ...
├── skills-repo/       # 部门 Skills（按业务分类）
│   └── dept-skills/
├── scripts/           # 管理脚本
├── templates/         # 配置模板
└── docs/              # 详细文档
```

## 文档

- [快速安装指南](docs/QUICKSTART.md)
- [配置说明](docs/CONFIG.md)
- [Agent 架构](docs/ARCHITECTURE.md)
- [Skills 管理](docs/SKILLS.md)
- [常见问题](docs/TROUBLESHOOTING.md)

## Agent 体系

| 部门 | Agent 数量 | 职责 |
|------|-----------|------|
| 高管层 | 1大+3小 | 战略决策、会议纪要 |
| 财务经营部 | 1大+3小 | 报表、预算、资金 |
| 国际交易部 | 1大+3小 | 国际贸易、外汇对冲 |
| 国内交易部 | 1大+3小 | 国内贸易、区域分析 |
| 交易执行部 | 1大+3小 | 订单执行、物流协调 |
| 汇率经营部 | 1大+3小 | 汇率风险、对冲策略 |
| 供应链运营部 | 1大+3小 | 供应链、库存、物流 |
| 期现交易部 | 1大+3小 | 期货交易、套利 |
| 卓越运营部 | 1大+3小 | 流程优化、KPI |
| 经营管理部 | 1大+3小 | 战略规划、绩效考核 |

## License

MIT
