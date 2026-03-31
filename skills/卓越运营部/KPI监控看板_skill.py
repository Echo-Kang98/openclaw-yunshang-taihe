"""
KPI监控看板 Skill - 卓越运营部
核心KPI实时监控、预警、可视化
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class KPIMonitoringSkill(BaseSkill):
    name = "KPI监控看板"
    description = "核心KPI实时监控、预警、可视化"
    department = "卓越运营部"
    
    trigger_keywords = ["KPI", "指标监控", "达成率", "KPI看板", "指标看板"]
    optional_keywords = ["查看", "分析", "监控"]
    examples = ["查看本月KPI", "KPI达成情况"]

    def parse_input(self, user_input: str) -> dict:
        return {"period": "monthly"}

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        return {
            "kpis": [
                {"name": "贸易量", "target": 50000, "actual": 46500, "rate": 93.0, "status": "🟡"},
                {"name": "营业收入", "target": 10000, "actual": 8920, "rate": 89.2, "status": "🟡"},
                {"name": "毛利率", "target": 5.0, "actual": 5.8, "rate": 116.0, "status": "🟢"},
                {"name": "回款天数", "target": 45, "actual": 42, "rate": 95.6, "status": "🟢"},
            ]
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        kpis = data["kpis"]
        on_target = sum(1 for k in kpis if k["status"] == "🟢")
        return {
            "type": "KPI监控看板",
            "overall_rate": round(sum(k["rate"] for k in kpis) / len(kpis), 1),
            "on_target": on_target,
            "kpi_list": kpis,
            "summary": f"共{len(kpis)}项KPI，{on_target}项达标，整体{sum(k['rate'] for k in kpis)/len(kpis):.1f}%",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "KPI数据已生成")
