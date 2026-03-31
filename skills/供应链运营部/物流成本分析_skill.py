"""
物流成本分析 Skill - 供应链运营部
运费结构分析、物流对标、路径优化、降本空间测算
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class LogisticsCostSkill(BaseSkill):
    name = "物流成本分析"
    description = "运费结构分析、物流对标、路径优化、降本空间测算"
    department = "供应链运营部"
    
    trigger_keywords = ["物流成本", "运费分析", "降本", "对标", "路径优化"]
    optional_keywords = ["分析", "查看", "建议"]
    examples = ["分析本月物流成本", "降本空间", "运费对标"]

    def parse_input(self, user_input: str) -> dict:
        return {"sub_skill": "overview"}

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        return {
            "total_cost": 285.0,
            "cost_per_ton": 28.5,
            "industry_avg": 32.0,
            "breakdown": {"海运费": 142, "陆运费": 57, "仓储": 43, "清关": 28, "保险": 15},
            "saving_potential": 15.0,
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        return {
            "type": "物流成本分析",
            "total": f"¥{data['total_cost']}万",
            "per_ton": f"¥{data['cost_per_ton']}/吨",
            "industry_avg": f"¥{data['industry_avg']}/吨",
            "vs_industry": f"-{abs(data['cost_per_ton']-data['industry_avg'])/data['industry_avg']*100:.1f}%",
            "saving": f"¥{data['saving_potential']}万/年",
            "summary": f"物流成本¥{data['total_cost']}万/吨，优于行业{data['vs_industry']}，可节省¥{data['saving_potential']}万/年",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "物流成本数据已生成")
