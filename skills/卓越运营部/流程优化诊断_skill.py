"""
流程优化诊断 Skill - 卓越运营部
流程瓶颈识别、优化方案、收益测算
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class ProcessOptimizationSkill(BaseSkill):
    name = "流程优化诊断"
    description = "流程瓶颈识别、优化方案、收益测算"
    department = "卓越运营部"
    
    trigger_keywords = ["流程优化", "瓶颈诊断", "流程再造", "效率提升", "优化方案"]
    optional_keywords = ["分析", "诊断", "优化"]
    examples = ["诊断流程瓶颈", "订单处理流程优化"]

    def parse_input(self, user_input: str) -> dict:
        params = {"process": "订单处理流程"}
        if re.search(r"采购|入库", user_input):
            params["process"] = "采购入库流程"
        elif re.search(r"审批|付款", user_input):
            params["process"] = "付款审批流程"
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        return {
            "process": params.get("process", "订单处理流程"),
            "total_hours": 72,
            "bottleneck": {"环节": "财务审批", "耗时": 36, "占比": "50%"},
            "steps": [
                {"name": "订单录入", "duration": 2},
                {"name": "风控审核", "duration": 8},
                {"name": "财务审批", "duration": 36},
                {"name": "执行发货", "duration": 20},
                {"name": "交付确认", "duration": 6},
            ],
            "saving_potential": 20,
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        return {
            "type": "流程优化诊断",
            "process": data["process"],
            "total_hours": f"{data['total_hours']}小时",
            "bottleneck": f"{data['bottleneck']['环节']}（占比{data['bottleneck']['占比']}）",
            "saving": f"{data['saving_potential']}小时（{data['saving_potential']/data['total_hours']*100:.0f}%）",
            "summary": f"{data['process']}总耗时{data['total_hours']}小时，瓶颈在{data['bottleneck']['环节']}",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "流程诊断已完成")
