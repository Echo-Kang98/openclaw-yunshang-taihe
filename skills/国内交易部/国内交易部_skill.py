"""
DomesticTrade Skill - 国内交易部综合技能
区域市场分析、国内供应商客户管理、国内市场情报收集、国内贸易执行
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class DomesticTradeSkill(BaseSkill):
    """
    国内交易部综合技能
    
    触发条件:
    - 用户说"国内交易"、"国内市场"
    - 用户说"区域市场"、"华东"、"华南"
    - 用户说"供应商"、"客户"、"渠道"
    - 用户说"市场情报"、"价格"、"供需"
    """

    name = "国内交易部综合技能"
    description = "区域市场分析、国内供应商客户管理、市场情报收集、国内贸易执行"
    department = "国内交易部"
    
    trigger_keywords = [
        "国内交易", "国内市场", "国内贸易",
        "区域市场", "华东", "华南", "华北",
        "供应商", "客户", "渠道",
        "市场情报", "价格", "供需",
        "国内采购", "国内销售",
    ]
    
    optional_keywords = [
        "分析", "查看", "管理", "收集", "执行",
    ]
    
    examples = [
        "分析华东市场价格走势",
        "查看国内供应商列表",
        "收集今日市场情报",
        "执行国内销售订单",
    ]

    def parse_input(self, user_input: str) -> dict:
        params = {"sub_skill": None}
        
        if re.search(r"区域市场|价格走势|市场分析", user_input):
            params["sub_skill"] = "market_analysis"
        elif re.search(r"供应商|客户|渠道", user_input):
            params["sub_skill"] = "supplier_customer"
        elif re.search(r"市场情报|情报收集|新闻", user_input):
            params["sub_skill"] = "intelligence"
        elif re.search(r"贸易执行|销售|采购|订单", user_input):
            params["sub_skill"] = "execution"
        
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        sub_skill = params.get("sub_skill")
        
        if sub_skill == "market_analysis":
            return self._mock_market_data(params)
        elif sub_skill == "supplier_customer":
            return self._mock_customer_data(params)
        elif sub_skill == "intelligence":
            return self._mock_intelligence_data(params)
        return self._mock_execution_data(params)

    def _mock_market_data(self, params: dict) -> dict:
        return {
            "regions": [
                {"name": "华东", "price": 3850, "change": 1.2, "supply": "平衡", "demand": "旺盛"},
                {"name": "华南", "price": 3820, "change": 0.8, "supply": "偏紧", "demand": "稳定"},
                {"name": "华北", "price": 3780, "change": -0.5, "supply": "充裕", "demand": "一般"},
            ]
        }

    def _mock_customer_data(self, params: dict) -> dict:
        return {
            "suppliers": [
                {"name": "山东地炼A", "grade": "A", "product": "柴油", "capacity": 10000, "delivery_rate": 98},
                {"name": "江苏化工B", "grade": "B", "product": "化工品", "capacity": 5000, "delivery_rate": 95},
            ],
            "customers": [
                {"name": "华东客户A", "grade": "VIP", "credit_limit": 500, "used": 230},
                {"name": "华南客户B", "grade": "A", "credit_limit": 200, "used": 85},
            ]
        }

    def _mock_intelligence_data(self, params: dict) -> dict:
        return {
            "price_updates": [
                {"product": "SC原油", "price": 625.5, "change": "+1.2%", "region": "全国"},
                {"product": "柴油", "price": 7850, "change": "+0.5%", "region": "华东"},
            ],
            "policy_alerts": [
                {"title": "发改委油价调整", "content": "下一轮调价预期上涨", "impact": "增加采购成本"}            ]
        }

    def _mock_execution_data(self, params: dict) -> dict:
        return {
            "orders": [
                {"no": "D-ORD-20260331-001", "type": "采购", "product": "柴油", "quantity": 500, "price": 7850, "status": "执行中"},
            ]
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        sub_skill = params.get("sub_skill")
        
        if sub_skill == "market_analysis":
            return {"type": "区域市场分析", "regions": data["regions"], "summary": "区域市场价格已更新"}
        elif sub_skill == "supplier_customer":
            return {"type": "供应商客户概览", "suppliers": data["suppliers"], "customers": data["customers"], "summary": f"供应商{len(data['suppliers'])}家，客户{len(data['customers'])}家"}
        elif sub_skill == "intelligence":
            return {"type": "市场情报", "updates": data["price_updates"], "alerts": data["policy_alerts"], "summary": f"情报{len(data['price_updates'])}条，政策预警{len(data['policy_alerts'])}条"}
        return {"type": "国内贸易执行", "orders": data["orders"], "summary": f"执行中订单{len(data['orders'])}笔"}

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "国内交易数据已生成")
