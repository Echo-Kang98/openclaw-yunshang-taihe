"""
国际供应商关系管理 Skill - 国际交易部
供应商开发、资质审核、绩效评估、合作维护
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class IntlSupplierSkill(BaseSkill):
    name = "国际供应商关系管理"
    description = "供应商开发、资质审核、绩效评估、合作维护"
    department = "国际交易部"
    
    trigger_keywords = ["国际供应商", "供应商关系", "供应商评估", "供应商绩效"]
    optional_keywords = ["查看", "分析", "管理", "评估"]
    examples = ["查看国际供应商列表", "供应商绩效评估"]

    def parse_input(self, user_input: str) -> dict:
        params = {"sub_skill": "overview"}
        if re.search(r"绩效|评估|评分", user_input):
            params["sub_skill"] = "performance"
        elif re.search(r"资质|审核|准入", user_input):
            params["sub_skill"] = "qualification"
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        return {
            "suppliers": [
                {"name": "阿联酋国家石油", "country": "阿联酋", "grade": "A", "main_product": "原油", "capacity": 50000, "delivery_rate": 98.5, "price_competitiveness": 85},
                {"name": "伊拉克国家石油", "country": "伊拉克", "grade": "B", "main_product": "原油", "capacity": 30000, "delivery_rate": 95.2, "price_competitiveness": 92},
                {"name": "卡塔尔天然气", "country": "卡塔尔", "grade": "A", "main_product": "LNG", "capacity": 20000, "delivery_rate": 99.1, "price_competitiveness": 78},
            ]
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        suppliers = data["suppliers"]
        a_count = sum(1 for s in suppliers if s["grade"] == "A")
        return {
            "type": "国际供应商概览",
            "total": len(suppliers),
            "a_grade": a_count,
            "supplier_list": suppliers,
            "summary": f"共{len(suppliers)}家供应商，A级{a_count}家",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "供应商数据已生成")
