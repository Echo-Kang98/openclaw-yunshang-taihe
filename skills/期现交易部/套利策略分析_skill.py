"""
套利策略分析 Skill - 期现交易部
跨期套利、跨品种套利、统计套利分析
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class ArbitrageStrategySkill(BaseSkill):
    name = "套利策略分析"
    description = "跨期套利、跨品种套利、统计套利分析"
    department = "期现交易部"
    
    trigger_keywords = ["套利策略", "跨期套利", "跨品种套利", "套利机会", "价差"]
    optional_keywords = ["分析", "查看", "建议"]
    examples = ["分析SC-Brent套利机会", "查看跨期套利"]

    def parse_input(self, user_input: str) -> dict:
        params = {"sub_skill": "overview"}
        if re.search(r"跨期|日历价差", user_input):
            params["sub_skill"] = "calendar"
        elif re.search(r"跨品种|跨市场", user_input):
            params["sub_skill"] = "intervariety"
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        sc_price = random.uniform(580, 650)
        brent_price = random.uniform(70, 85) * 7.2
        spread = sc_price - brent_price
        z_score = (spread - 25) / 15
        return {
            "sc_price": round(sc_price, 1),
            "brent_price_cny": round(brent_price, 1),
            "spread": round(spread, 1),
            "z_score": round(z_score, 2),
            "signal": "观望" if abs(z_score) < 1.5 else ("买入SC/卖出Brent" if z_score < -1.5 else "观望"),
            "confidence": 0.75 if abs(z_score) > 2 else 0.4,
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        return {
            "type": "套利策略分析",
            "spread": f"¥{data['spread']}元/桶",
            "z_score": data["z_score"],
            "signal": data["signal"],
            "confidence": f"{data['confidence']*100:.0f}%",
            "summary": f"SC-Brent价差¥{data['spread']}，Z-score={data['z_score']}，信号：{data['signal']}",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "套利分析已完成")
