"""
资金调度管理 Skill - 财务经营部
资金池监控、闲置资金管理、现金流预测
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class CapitalDispatchSkill(BaseSkill):
    name = "资金调度管理"
    description = "资金池监控、闲置资金管理、现金流预测"
    department = "财务经营部"
    
    trigger_keywords = ["资金调度", "资金池", "闲置资金", "现金流预测", "资金管理"]
    optional_keywords = ["查看", "分析", "建议"]
    examples = ["查看资金状态", "闲置资金建议"]

    def parse_input(self, user_input: str) -> dict:
        return {}

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        return {
            "total_balance": 5680.5,
            "idle_funds": 1200.0,
            "utilization_rate": 78.9,
            "suggestion": "投入3个月理财，预期收益2.8%/年",
            "cash_flow_7d": {"inflow": 2500, "outflow": 1800, "net": 700},
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        return {
            "type": "资金调度概览",
            "total": f"¥{data['total_balance']}万",
            "idle": f"¥{data['idle_funds']}万",
            "utilization": f"{data['utilization_rate']}%",
            "suggestion": data["suggestion"],
            "cash_flow_7d": f"净流入¥{data['cash_flow_7d']['net']}万",
            "summary": f"余额¥{data['total_balance']}万，闲置¥{data['idle_funds']}万，利用率{data['utilization_rate']}%",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "资金数据已生成")
