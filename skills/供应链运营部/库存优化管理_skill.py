"""
库存优化管理 Skill - 供应链运营部
库存结构分析、安全库存计算、呆滞库存处理、补货策略
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class InventoryOptimizationSkill(BaseSkill):
    name = "库存优化管理"
    description = "库存结构分析、安全库存计算、呆滞库存处理、补货策略"
    department = "供应链运营部"
    
    trigger_keywords = [
        "库存优化", "安全库存", "呆滞库存",
        "库存周转", "ABC分类", "补货",
        "库存分析", "库存结构",
    ]
    optional_keywords = ["分析", "查看", "优化", "建议"]
    examples = ["分析库存结构", "查看呆滞库存", "补货建议"]

    def parse_input(self, user_input: str) -> dict:
        params = {"sub_skill": "overview"}
        if re.search(r"安全库存|补货", user_input):
            params["sub_skill"] = "reorder"
        elif re.search(r"呆滞", user_input):
            params["sub_skill"] = "slow_moving"
        elif re.search(r"ABC|分类", user_input):
            params["sub_skill"] = "abc"
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        return {
            "total": 85000,
            "turnover_rate": 8.5,
            "turnover_days": 43,
            "slow_moving_ratio": 3.2,
            "abc": {"A": 60, "B": 25, "C": 15},
            "slow_moving_items": [
                {"product": "沥青A", "quantity": 1200, "days": 220},
                {"product": "重油B", "quantity": 800, "days": 180},
            ],
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        return {
            "type": "库存分析报告",
            "total": f"{data['total']:,}吨",
            "turnover_rate": f"{data['turnover_rate']}次/年",
            "slow_moving_ratio": f"{data['slow_moving_ratio']}%",
            "abc": data["abc"],
            "summary": f"总库存{data['total']:,}吨，周转{data['turnover_rate']}次/年，呆滞率{data['slow_moving_ratio']}%",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "库存数据已生成")
