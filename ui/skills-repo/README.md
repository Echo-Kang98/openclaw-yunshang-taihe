# Skills Repository - 泰和嘉柏云上2.0

> 参考 ClawHub 模式构建的 Skills 仓库

## 目录结构

```
skills-repo/
├── README.md              # 本文件
├── dept-skills/           # 各部门专属技能
│   ├── executive/         # 高管层
│   ├── finance/           # 财务经营部
│   ├── international-trade/ # 国际交易部
│   ├── domestic-trade/    # 国内交易部
│   ├── trading-execution/ # 交易执行部
│   ├── fx-operation/      # 汇率经营部
│   ├── supply-chain/       # 供应链运营部
│   ├── futures-spot/       # 期现交易部
│   ├── excellence-ops/     # 卓越运营部
│   └── mgmt-ops/           # 经营管理部
└── global-skills/         # 全局基础技能（通用）
```

## Skills 规范

每个 Skill 目录包含：
- `SKILL.md` - Skill定义（名称、描述、参数）
- `scripts/` - 技能执行脚本
- `references/` - 参考文档

## 已配置的Skills

| 部门 | 技能数 | 激活数 |
|------|--------|--------|
| 高管层 | 3 | 2 |
| 财务经营部 | 5 | 3 |
| 国际交易部 | 5 | 4 |
| 国内交易部 | 4 | 3 |
| 交易执行部 | 5 | 4 |
| 汇率经营部 | 4 | 3 |
| 供应链运营部 | 4 | 3 |
| 期现交易部 | 5 | 4 |
| 卓越运营部 | 3 | 2 |
| 经营管理部 | 4 | 3 |
| 全局基础 | 3 | 3 |
| **合计** | **45** | **34** |

## 使用方式

Skills 通过后台管理界面统一配置，支持：
- 新增技能
- 编辑技能
- 启用/禁用技能
- 按部门/分类筛选
- 分配给Agent

## 扩展指南

参考 ClawHub 模式：
1. 在 `dept-skills/` 下创建部门目录
2. 编写 `SKILL.md` 定义技能
3. 在管理后台添加技能记录
4. 分配给对应Agent使用
