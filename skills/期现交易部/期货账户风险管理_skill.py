"""
期货账户风险管理 Skill - 期现交易部
保证金监控、持仓限额、清算管理
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class FuturesRiskSkill(BaseSkill):
    name = "期货账户风险管理"
    description = "保证金监控、持仓限额、清算管理"
    department = "期现交易部"
    
    trigger_keywords = ["期货风险", "保证金", "持仓限额", "强平", "追保", "账户风险"]
    optional_keywords = ["查看", "监控", "分析"]
    examples = ["查看保证金状态", "期货账户风险报告"]

    def parse_input(self, user_input: str) -> dict:
        return {}

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        margin = random.randint(2500, 3500)
        balance = 5000
        return {
            "balance": balance,
            "margin_used": margin,
            "available": balance - margin,
            "risk_level": round(margin / balance * 100, 1),
            "risk_status": "🟢正常" if margin/balance < 0.5 else "🟡关注" if margin/balance < 0.8 else "🟠预警",
            "positions": [
                {"variety": "SC", "direction": "long", "qty": 10, "open_price": 620, "current_price": 615},
            ]
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        return {
            "type": "期货账户风险报告",
            "balance": f"¥{data['balance']}万",
            "margin_used": f"¥{data['margin_used']}万",
            "available": f"¥{data['available']}万",
            "risk_level": f"{data['risk_level']}%",
            "status": data["risk_status"],
            "summary": f"风险度{data['risk_level']}%，{data['risk_status']}，可用¥{data['available']}万",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "期货风险数据已生成")
