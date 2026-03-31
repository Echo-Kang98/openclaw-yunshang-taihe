"""
仓储管理 Skill - 供应链运营部
罐区管理、出入库操作、安全管理、库存台账、损耗分析
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class WarehouseSkill(BaseSkill):
    name = "仓储管理"
    description = "罐区管理、出入库操作、安全管理、库存台账、损耗分析"
    department = "供应链运营部"
    
    trigger_keywords = [
        "仓储", "罐区", "入库", "出库",
        "库存台账", "盘点", "液位",
        "安全管理", "防溢", "损耗",
        "仓储管理",
    ]
    optional_keywords = ["查看", "分析", "监控"]
    examples = ["查看罐区液位状态", "分析本月损耗", "出入库记录"]

    def parse_input(self, user_input: str) -> dict:
        params = {"sub_skill": "overview"}
        if re.search(r"罐区|液位|温度", user_input):
            params["sub_skill"] = "tank"
        elif re.search(r"出入库|入库|出库", user_input):
            params["sub_skill"] = "inout"
        elif re.search(r"损耗|损耗分析", user_input):
            params["sub_skill"] = "loss"
        elif re.search(r"安全|预警", user_input):
            params["sub_skill"] = "safety"
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        return {
            "tanks": [
                {"tank_id": "T-001", "product": "SC原油", "level": 85.5, "capacity": 50000, "temperature": 28.5, "status": "正常"},
                {"tank_id": "T-002", "product": "Brent", "level": 62.3, "capacity": 30000, "temperature": 25.2, "status": "正常"},
                {"tank_id": "T-003", "product": "航空煤油", "level": 45.0, "capacity": 20000, "temperature": 22.0, "status": "正常"},
            ],
            "utilization": 68.4,
            "today_in": 3500,
            "today_out": 2800,
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        tanks = data["tanks"]
        return {
            "type": "仓储状态",
            "utilization": f"{data['utilization']}%",
            "today_in": f"{data['today_in']}吨",
            "today_out": f"{data['today_out']}吨",
            "tank_count": len(tanks),
            "summary": f"罐区利用率{data['utilization']}%，今日入库{data['today_in']}吨，出库{data['today_out']}吨",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "仓储数据已生成")
