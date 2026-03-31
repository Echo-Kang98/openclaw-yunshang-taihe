"""
供应链管理 Skill - 供应链运营部
供应链可视化、供应商协同VMI、风险预警、协调会议
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class SupplyChainMgmtSkill(BaseSkill):
    name = "供应链管理"
    description = "供应链可视化、供应商协同VMI、风险预警、协调会议"
    department = "供应链运营部"
    
    trigger_keywords = [
        "供应链", "供应商协同", "VMI",
        "风险预警", "供应链协调", "例会",
        "断供预警", "供应风险",
    ]
    optional_keywords = ["查看", "分析", "协调", "预警"]
    examples = ["查看供应链状态", "分析供应风险", "VMI协同报告"]

    def parse_input(self, user_input: str) -> dict:
        params = {"sub_skill": "overview"}
        if re.search(r"VMI|供应商协同", user_input):
            params["sub_skill"] = "vmi"
        elif re.search(r"风险|预警|断供", user_input):
            params["sub_skill"] = "risk"
        elif re.search(r"例会|会议|协调", user_input):
            params["sub_skill"] = "meeting"
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        return {
            "risk_level": "🟢 低风险",
            "suppliers": 12,
            "on_time_rate": 95.5,
            "vmi_partners": 3,
            "risks": [],
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        return {
            "type": "供应链概览",
            "risk_level": data["risk_level"],
            "suppliers": data["suppliers"],
            "on_time_rate": f"{data['on_time_rate']}%",
            "vmi_partners": data["vmi_partners"],
            "summary": f"风险{data['risk_level']}，供应商{data['suppliers']}家，准时率{data['on_time_rate']}%",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "供应链数据已生成")
