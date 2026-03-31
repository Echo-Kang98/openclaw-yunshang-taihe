"""
预算执行监控 Skill - 财务经营部
预算执行跟踪、偏差分析、预警
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class BudgetExecutionSkill(BaseSkill):
    name = "预算执行监控"
    description = "预算执行跟踪、偏差分析、预警"
    department = "财务经营部"
    
    trigger_keywords = ["预算执行", "预算监控", "执行率", "偏差分析", "预算预警"]
    optional_keywords = ["查看", "分析", "监控"]
    examples = ["查看预算执行情况", "偏差分析"]

    def parse_input(self, user_input: str) -> dict:
        return {}

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        return {
            "total_budget": 15000,
            "executed": 8920.5,
            "execution_rate": 59.5,
            "status": "🟡正常",
            "items": [
                {"name": "收入", "budget": 50000, "executed": 38500, "rate": 77.0},
                {"name": "成本", "budget": 42000, "executed": 32800, "rate": 78.1},
                {"name": "费用", "budget": 3000, "executed": 1890, "rate": 63.0},
            ]
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        return {
            "type": "预算执行监控",
            "execution_rate": f"{data['execution_rate']}%",
            "status": data["status"],
            "executed": f"¥{data['executed']}万",
            "budget": f"¥{data['total_budget']}万",
            "item_list": data["items"],
            "summary": f"预算执行率{data['execution_rate']}%，{data['status']}",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "预算执行数据已生成")
