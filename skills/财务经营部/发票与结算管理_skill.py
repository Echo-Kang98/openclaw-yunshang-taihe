"""
发票与结算管理 Skill - 财务经营部
发票开具、核对、结算付款
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class InvoiceSettlementSkill(BaseSkill):
    name = "发票与结算管理"
    description = "发票开具、核对、结算付款"
    department = "财务经营部"
    
    trigger_keywords = ["发票", "结算", "付款", "收款", "应收", "应付"]
    optional_keywords = ["查看", "管理", "分析"]
    examples = ["查看发票状态", "本月结算情况"]

    def parse_input(self, user_input: str) -> dict:
        params = {"sub_skill": "overview"}
        if re.search(r"应收|收款", user_input):
            params["sub_skill"] = "receivable"
        elif re.search(r"应付|付款", user_input):
            params["sub_skill"] = "payable"
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        return {
            "receivables": [
                {"customer": "华东客户A", "amount": 580, "due_date": "2026-04-15", "status": "正常"},
                {"customer": "华南客户B", "amount": 260, "due_date": "2026-04-20", "status": "逾期"},
            ],
            "total_receivable": 8920.5,
            "overdue": 168.9,
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        return {
            "type": "发票结算概览",
            "total_receivable": f"¥{data['total_receivable']}万",
            "overdue": f"¥{data['overdue']}万",
            "receivable_list": data["receivables"],
            "summary": f"应收账款¥{data['total_receivable']}万，逾期¥{data['overdue']}万",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "发票结算数据已生成")
