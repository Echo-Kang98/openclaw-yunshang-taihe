"""
国际贸易合同管理 Skill - 国际交易部
合同起草、审阅、履约跟踪
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class IntlContractSkill(BaseSkill):
    name = "国际贸易合同管理"
    description = "合同起草、审阅、履约跟踪"
    department = "国际交易部"
    
    trigger_keywords = ["国际贸易合同", "合同审阅", "合同履约", "合同条款", "FOB合同", "CIF合同"]
    optional_keywords = ["查看", "审核", "跟踪", "起草"]
    examples = ["查看合同执行状态", "审核国际贸易合同"]

    def parse_input(self, user_input: str) -> dict:
        params = {"sub_skill": "overview"}
        if re.search(r"起草|新建", user_input):
            params["sub_skill"] = "draft"
        elif re.search(r"审阅|审核", user_input):
            params["sub_skill"] = "review"
        elif re.search(r"跟踪|履约", user_input):
            params["sub_skill"] = "track"
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        return {
            "contracts": [
                {"no": "CTR-2026-0301", "supplier": "阿联酋国家石油", "product": "原油", "quantity": 50000, "price": 82.5, "term": "FOB", "status": "执行中", "delivery": "2026-04-15"},
                {"no": "CTR-2026-0228", "supplier": "卡塔尔天然气", "product": "LNG", "quantity": 20000, "price": 10.5, "term": "CIF", "status": "待发货", "delivery": "2026-04-20"},
            ]
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        contracts = data["contracts"]
        active = [c for c in contracts if c["status"] == "执行中"]
        return {
            "type": "国际贸易合同概览",
            "total": len(contracts),
            "active": len(active),
            "contract_list": contracts,
            "summary": f"共{len(contracts)}份合同，{len(active)}份执行中",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "合同数据已生成")
