"""
期现对冲策略 Skill - 期现交易部
现货敞口分析、套保比率、合约选择、动态调整
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class SpotFuturesHedgingSkill(BaseSkill):
    name = "期现对冲策略"
    description = "现货敞口分析、套保比率、合约选择、动态调整"
    department = "期现交易部"
    
    trigger_keywords = ["期现对冲", "套保比率", "现货对冲", "对冲策略"]
    optional_keywords = ["分析", "建议", "设计"]
    examples = ["设计一个期现对冲方案", "分析套保比率"]

    def parse_input(self, user_input: str) -> dict:
        params = {}
        if re.search(r"采购|买保|买入对冲", user_input):
            params["hedge_type"] = "buy"
        elif re.search(r"销售|卖保|卖出对冲", user_input):
            params["hedge_type"] = "sell"
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        spot = random.uniform(580, 650)
        return {
            "spot_price": round(spot, 1),
            "futures_price": round(spot * 1.02, 1),
            "basis": round(spot * 0.02, 1),
            "hedge_ratio": 0.9,
            "recommended_contracts": 10,
            "effectiveness": "85%",
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        return {
            "type": "期现对冲策略",
            "spot_price": f"¥{data['spot_price']}元/桶",
            "futures_price": f"¥{data['futures_price']}元/桶",
            "basis": f"¥{data['basis']}元/桶",
            "hedge_ratio": data["hedge_ratio"],
            "contracts": data["recommended_contracts"],
            "effectiveness": data["effectiveness"],
            "summary": f"建议对冲比例{data['hedge_ratio']}，需{data['recommended_contracts']}手期货，对冲效率{data['effectiveness']}",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "期现对冲策略已生成")
