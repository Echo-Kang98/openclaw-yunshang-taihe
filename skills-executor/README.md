# Skills执行框架

> 云上泰和2.0项目 - 工部出品

为云上泰和2.0的41个Skill提供统一的Python执行框架。

## 📁 目录结构

```
skills-executor/
├── __init__.py              # 包入口
├── base.py                  # BaseSkill基类
├── skill_loader.py          # SKILL.md解析器
├── runner.py                # 统一执行入口
├── tools/                   # 工具函数
│   ├── __init__.py
│   ├── fetch_weather.py      # 天气查询（预留API）
│   ├── send_message.py       # 消息发送（预留API）
│   └── formatters.py         # 格式化工具
└── skills/                  # 各Skill实现
    ├── __init__.py
    ├── 财务经营部/
    │   ├── __init__.py
    │   └── financial_report.py    # 财务报表生成
    ├── 期现交易部/
    │   ├── __init__.py
    │   └── futures_trading.py      # 期货交易执行
    └── 汇率经营部/
        ├── __init__.py
        └── exchange_rate.py        # 汇率走势分析
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd skills-executor
pip install -r requirements.txt  # 无外部依赖，纯标准库
```

### 2. 运行示例

```bash
# 财务报表生成
python runner.py "生成2026年1月财务报表"

# 期货交易执行
python runner.py "SC原油608元/桶买入开仓10手"

# 汇率走势分析
python runner.py "分析美元/人民币走势"
```

### 3. 列出所有Skill

```bash
python runner.py --list
python runner.py --load   # 同时解析SKILL.md
```

## 📋 已实现的核心Skill

### A. 财务报表生成 (FinancialReportSkill)

**触发条件**:
- "生成月度财务报表"
- "看看本月P&L"
- "审计需要的定期报告"

**输入参数**:
- `period`: 期间 (2026-01, 2026-Q1, 2026)
- `report_type`: 月报/月度/季报/年报

**输出**:
```json
{
  "report_type": "财务报表",
  "period": "2026年1月",
  "income_statement": { ... },
  "balance_sheet": { ... },
  "cash_flow": { ... },
  "kpis": { ... }
}
```

### B. 期货交易执行 (FuturesTradingSkill)

**触发条件**:
- "在SC原油期货上建10手多头"
- "平掉全部Brent空头仓位"

**输入参数**:
- `variety`: 品种 (SC/BRENT/WTI/DUBAI)
- `direction`: 方向 (long/short)
- `quantity`: 数量 (手)
- `price`: 价格 (可选)

**输出**:
```json
{
  "report_type": "期货交易执行报告",
  "trade_order": { ... },
  "execution_record": { ... },
  "current_position": { ... },
  "risk_alert": "..."
}
```

### C. 汇率走势分析 (ExchangeRateAnalysisSkill)

**触发条件**:
- "美元/人民币接下来怎么走"
- "分析EUR/USD走势"

**输入参数**:
- `pair`: 货币对 (USD/CNY, EUR/USD等)
- `horizon`: 周期 (short/medium/both)

**输出**:
```json
{
  "report_type": "汇率走势分析报告",
  "rate现状": { ... },
  "drivers": { ... },
  "technical": { ... },
  "forecast": { ... },
  "trade_advice": { ... }
}
```

## 🏗️ 框架设计

### BaseSkill基类

所有Skill继承自`BaseSkill`，实现以下核心方法:

```python
class BaseSkill:
    name: str = "Skill名称"
    department: str = "所属部门"
    trigger_keywords: list = ["触发词1", "触发词2"]
    optional_keywords: list = ["可选词"]
    
    def can_handle(self, user_input: str) -> bool:
        """判断是否处理该输入"""
        
    async def execute(self, context: dict) -> SkillResult:
        """执行Skill"""
        
    def parse_input(self, user_input: str) -> dict:
        """解析用户输入"""
        
    async def fetch_data(self, params: dict, context: dict) -> dict:
        """获取数据（预留API）"""
        
    def generate_output(self, data: dict, params: dict) -> dict:
        """生成输出"""
```

### SkillResult标准化输出

```python
@dataclass
class SkillResult:
    success: bool
    skill_name: str
    output_format: OutputFormat
    data: Any           # 主数据
    summary: str        # 一句话摘要
    error: Optional[str]
    execution_time_ms: float
    metadata: dict
```

## 🔧 扩展新Skill

1. **创建Skill文件**:
```python
# skills/新部门/new_skill.py
from base import BaseSkill, SkillResult

class NewSkill(BaseSkill):
    name = "新技能"
    department = "新部门"
    trigger_keywords = ["触发词"]
    
    def parse_input(self, user_input: str) -> dict:
        # 解析参数
        return {"param": value}
    
    async def fetch_data(self, params: dict, context: dict) -> dict:
        # TODO: 接入真实API
        return {"mock": True}
    
    def generate_output(self, data: dict, params: dict) -> dict:
        return {"result": "..."}
```

2. **注册到runner.py**:
```python
from skills.新部门.new_skill import NewSkill
REGISTERED_SKILLS.append(NewSkill())
```

## 📌 预留API接口

| 模块 | 接口 | 状态 | 说明 |
|------|------|------|------|
| fetch_weather | 天气查询 | 预留 | 可接入wttr.in/Open-Meteo |
| send_message | 消息发送 | 预留 | 飞书/企微webhook |
| financial_report | 财务报表 | 预留 | 需接入ERP系统 |
| futures_trading | 期货交易 | 预留 | 需接入期货CTP API |
| exchange_rate | 汇率数据 | 预留 | 需接入Wind/Bloomberg |

## 📝 开发规范

1. **异步优先**: `execute()`和`fetch_data()`必须是`async`函数
2. **模拟数据**: 真实API接入前使用模拟数据，并在TODO注释中标注
3. **标准化输出**: 所有输出必须通过`generate_output()`转换为标准格式
4. **错误处理**: 使用`SkillResult`的错误字段，不要抛异常

## 🔗 相关文档

- [SKILL.md规范](./skills-repo/)
- [云上泰和2.0主仓库](https://github.com/Echo-Kang98/openclaw-yunshang-taihe)

---

**工部出品** | 云上泰和2.0 | 2026
