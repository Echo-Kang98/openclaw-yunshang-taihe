"""
InternationalTrade Skill - 国际交易部综合技能
管理国际供应商关系、国际贸易合同、国际贸易执行、外汇对冲策略
"""

import re
import asyncio
import random
from datetime import datetime, timedelta
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class InternationalTradeSkill(BaseSkill):
    """
    国际交易部综合技能
    
    触发条件:
    - 用户说"国际"、"进口"、"出口"、"跨国"
    - 用户说"供应商"、"合同"、"贸易条款"
    - 用户说"FOB"、"CIF"、"外汇"、"对冲"
    """

    name = "国际交易部综合技能"
    description = "管理国际供应商关系、国际贸易合同、外汇对冲策略"
    department = "国际交易部"
    
    trigger_keywords = [
        "国际", "进口", "出口", "跨国",
        "供应商", "合同", "贸易条款",
        "FOB", "CIF", "CFR", "EXW",
        "外汇", "汇率", "对冲", "USD", "EUR",
        "国际交易", "国际贸易",
    ]
    
    optional_keywords = [
        "管理", "分析", "执行", "监控", "审核",
    ]
    
    examples = [
        "查看国际供应商列表",
        "分析当前外汇对冲策略",
        "审核国际贸易合同",
    ]

    def parse_input(self, user_input: str) -> dict:
        params = {
            "sub_skill": None,  # supplier/contract/execution/forex
            "action": None,
        }
        
        if re.search(r"供应商|客户|关系", user_input):
            params["sub_skill"] = "supplier"
        elif re.search(r"合同|条款|协议", user_input):
            params["sub_skill"] = "contract"
        elif re.search(r"外汇|汇率|对冲", user_input):
            params["sub_skill"] = "forex"
        elif re.search(r"执行|发货|装运|清关", user_input):
            params["sub_skill"] = "execution"
        
        if re.search(r"查看|列表|分析|评估", user_input):
            params["action"] = "view"
        elif re.search(r"审核|审批|新建|创建", user_input):
            params["action"] = "create"
        
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        sub_skill = params.get("sub_skill")
        
        if sub_skill == "supplier":
            return self._mock_supplier_data(params)
        elif sub_skill == "contract":
            return self._mock_contract_data(params)
        elif sub_skill == "forex":
            return self._mock_forex_data(params)
        return self._mock_execution_data(params)

    def _mock_supplier_data(self, params: dict) -> dict:
        return {
            "suppliers": [
                {"name": "阿联酋国家石油", "country": "阿联酋", "grade": "A", "main_product": "原油", "capacity": 50000, "delivery_rate": 98.5},
                {"name": "伊拉克国家石油", "country": "伊拉克", "grade": "B", "main_product": "原油", "capacity": 30000, "delivery_rate": 95.2},
                {"name": "卡塔尔天然气", "country": "卡塔尔", "grade": "A", "main_product": "LNG", "capacity": 20000, "delivery_rate": 99.1},
            ]
        }

    def _mock_contract_data(self, params: dict) -> dict:
        return {
            "contracts": [
                {"no": "CTR-2026-0301", "supplier": "阿联酋国家石油", "product": "原油", "quantity": 50000, "price": 82.5, "term": "FOB", "status": "执行中", "delivery": "2026-04-15"},
                {"no": "CTR-2026-0228", "supplier": "卡塔尔天然气", "product": "LNG", "quantity": 20000, "price": 10.5, "term": "CIF", "status": "待发货", "delivery": "2026-04-20"},
            ]
        }

    def _mock_forex_data(self, params: dict) -> dict:
        return {
            "usd_cny": 7.25,
            "eur_cny": 7.85,
            "usd_rate": 0.45,
            "eur_rate": 0.15,
            "forward_1m": 7.27,
            "forward_3m": 7.32,
            "exposure_usd": 5000,
            "exposure_eur": 1000,
            "hedge_ratio": 0.75,
        }

    def _mock_execution_data(self, params: dict) -> dict:
        return {
            "shipments": [
                {"vessel": "MV TANKER A", "product": "原油", "quantity": 45000, "load_port": "Kuwait", "status": "航行中", "eta": "2026-04-10"},
                {"vessel": "MV TANKER B", "product": "LNG", "quantity": 18000, "load_port": "Qatar", "status": "装港", "eta": "2026-04-15"},
            ]
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        sub_skill = params.get("sub_skill")
        
        if sub_skill == "supplier":
            return self._generate_supplier_output(data, params)
        elif sub_skill == "contract":
            return self._generate_contract_output(data, params)
        elif sub_skill == "forex":
            return self._generate_forex_output(data, params)
        return self._generate_execution_output(data, params)

    def _generate_supplier_output(self, data: dict, params: dict) -> dict:
        suppliers = data["suppliers"]
        total = len(suppliers)
        a_grade = sum(1 for s in suppliers if s["grade"] == "A")
        return {
            "type": "国际供应商概览",
            "total_count": total,
            "a_grade_count": a_grade,
            "supplier_list": suppliers,
            "summary": f"共有{total}家国际供应商，其中A 级{a_grade}家",
        }

    def _generate_contract_output(self, data: dict, params: dict) -> dict:
        contracts = data["contracts"]
        total_amount = sum(c["quantity"] * c["price"] for c in contracts)
        return {
            "type": "国际贸易合同概览",
            "total_contracts": len(contracts),
            "total_amount_usd": round(total_amount, 1),
            "contract_list": contracts,
            "summary": f"共有{len(contracts)}份执行中合同，总金额约${total_amount:,.0f}万",
        }

    def _generate_forex_output(self, data: dict, params: dict) -> dict:
        return {
            "type": "外汇敞口与对冲概览",
            "usd_cny": data["usd_cny"],
            "eur_cny": data["eur_cny"],
            "usd_exposure": f"${data['exposure_usd']}万",
            "eur_exposure": f"€{data['exposure_eur']}万",
            "hedge_ratio": data["hedge_ratio"],
            "summary": f"USD/CNY {data['usd_cny']}，USD敞口${data['exposure_usd']}万，对冲比例{data['hedge_ratio']*100:.0f}%",
        }

    def _generate_execution_output(self, data: dict, params: dict) -> dict:
        shipments = data["shipments"]
        return {
            "type": "国际贸易执行概览",
            "total_shipments": len(shipments),
            "on_water": sum(1 for s in shipments if s["status"] == "航行中"),
            "at_port": sum(1 for s in shipments if s["status"] in ["装港", "卸港"]),
            "shipment_list": shipments,
            "summary": f"共{len(shipments)}船货物，{sum(1 for s in shipments if s['status']=='航行中')}船航行中",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "国际交易数据已生成")
