"""
经营态势日报 Skill - 高管层
每日经营关键信息汇总
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class BusinessDailyReportSkill(BaseSkill):
    name = "经营态势日报"
    description = "每日经营关键信息汇总"
    department = "高管层"
    
    trigger_keywords = ["经营日报", "态势日报", "每日简报", "日报"]
    optional_keywords = ["生成", "查看"]
    examples = ["生成今日经营日报", "查看今日态势"]

    def parse_input(self, user_input: str) -> dict:
        return {}

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "key_highlights": [
                "SC原油期货上涨1.2%，收于625元/桶",
                "华东客户A订单完成交付，金额580万",
                "新签国际供应商合同CTR-20260331-001",
            ],
            "trade_volume": 15600,
            "revenue_daily": 2850.5,
            "risk_alerts": [],
            "sc_price": 625.5,
            "brent_price": 72.5,
            "usd_cny": 7.25,
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        return {
            "type": "经营态势日报",
            "date": data["date"],
            "highlights": data["key_highlights"],
            "trade_volume": f"{data['trade_volume']}吨",
            "revenue": f"¥{data['revenue_daily']}万",
            "sc_price": f"¥{data['sc_price']}",
            "brent_price": f"${data['brent_price']}",
            "usd_cny": data["usd_cny"],
            "alerts": data["risk_alerts"],
            "summary": f"{data['date']}日报：贸易量{data['trade_volume']}吨，收入¥{data['revenue_daily']}万，{data['highlights'][0]}",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "日报已生成")
