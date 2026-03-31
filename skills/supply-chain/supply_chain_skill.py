"""
SupplyChain Skill - 供应链运营部综合技能
管理仓储管理、供应链管理、库存优化、物流成本分析
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class SupplyChainSkill(BaseSkill):
    """
    供应链运营部综合技能
    
    触发条件:
    - 用户说"仓储"、"库存"、"入库"、"出库"
    - 用户说"供应链"、"物流"、"运输"
    - 用户说"库存周转"、"呆滞"、"盘点"
    - 用户说"运费"、"物流成本"、"降本"
    """

    name = "供应链运营部综合技能"
    description = "仓储管理、供应链协调、库存优化、物流成本分析"
    department = "供应链运营部"
    
    trigger_keywords = [
        "仓储", "库存", "入库", "出库",
        "供应链", "物流", "运输",
        "库存周转", "呆滞", "盘点",
        "运费", "物流成本", "降本",
        "供应链运营",
    ]
    
    optional_keywords = [
        "查看", "分析", "优化", "监控",
    ]
    
    examples = [
        "查看当前仓储状态",
        "分析本月物流成本",
        "优化库存结构建议",
    ]

    def parse_input(self, user_input: str) -> dict:
        params = {"sub_skill": None}
        
        if re.search(r"仓储|罐区|入库|出库", user_input):
            params["sub_skill"] = "warehouse"
        elif re.search(r"供应链|协同|协调", user_input):
            params["sub_skill"] = "supply_chain"
        elif re.search(r"库存周转|呆滞|库存优化|安全库存", user_input):
            params["sub_skill"] = "inventory"
        elif re.search(r"物流成本|运费|降本", user_input):
            params["sub_skill"] = "logistics_cost"
        
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        sub_skill = params.get("sub_skill")
        
        if sub_skill == "warehouse":
            return self._mock_warehouse_data(params)
        elif sub_skill == "supply_chain":
            return self._mock_supply_chain_data(params)
        elif sub_skill == "inventory":
            return self._mock_inventory_data(params)
        return self._mock_logistics_cost_data(params)

    def _mock_warehouse_data(self, params: dict) -> dict:
        return {
            "tanks": [
                {"tank_id": "T-001", "product": "SC原油", "level": 85.5, "capacity": 50000, "temperature": 28.5},
                {"tank_id": "T-002", "product": "Brent", "level": 62.3, "capacity": 30000, "temperature": 25.2},
                {"tank_id": "T-003", "product": "航空煤油", "level": 45.0, "capacity": 20000, "temperature": 22.0},
            ],
            "total_utilization": 68.4,
        }

    def _mock_supply_chain_data(self, params: dict) -> dict:
        return {
            "suppliers_count": 12,
            "on_time_rate": 95.5,
            "inventory_days": 18,
            "order_fulfillment_rate": 98.2,
            "supply_chain_risk": "🟢 低风险",
        }

    def _mock_inventory_data(self, params: dict) -> dict:
        return {
            "total_inventory": 85000,
            "turnover_rate": 8.5,
            "turnover_days": 43,
            "slow_moving_ratio": 3.2,
            "safety_stock": 12000,
            "abc_classification": {"A": 60, "B": 25, "C": 15},
        }

    def _mock_logistics_cost_data(self, params: dict) -> dict:
        return {
            "total_cost": 2850.0,
            "cost_breakdown": {
                "sea_freight": 1425.0,
                "land_freight": 570.0,
                "warehouse": 427.5,
                "customs": 285.0,
                "insurance": 142.5,
            },
            "cost_per_ton": 28.5,
            "industry_avg": 32.0,
            "vs_industry": -10.9,
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        sub_skill = params.get("sub_skill")
        
        if sub_skill == "warehouse":
            return self._generate_warehouse_output(data, params)
        elif sub_skill == "supply_chain":
            return self._generate_supply_chain_output(data, params)
        elif sub_skill == "inventory":
            return self._generate_inventory_output(data, params)
        return self._generate_logistics_cost_output(data, params)

    def _generate_warehouse_output(self, data: dict, params: dict) -> dict:
        tanks = data["tanks"]
        return {
            "type": "仓储状态概览",
            "total_utilization": f"{data['total_utilization']}%",
            "tank_count": len(tanks),
            "tank_list": tanks,
            "summary": f"罐区总利用率{data['total_utilization']}%，{len(tanks)}个储罐运行中",
        }

    def _generate_supply_chain_output(self, data: dict, params: dict) -> dict:
        return {
            "type": "供应链健康度",
            "suppliers_count": data["suppliers_count"],
            "on_time_rate": f"{data['on_time_rate']}%",
            "order_fulfillment_rate": f"{data['order_fulfillment_rate']}%",
            "risk_status": data["supply_chain_risk"],
            "summary": f"供应链整体{data['supply_chain_risk']}，供应商{data['suppliers_count']}家，准时率{data['on_time_rate']}%",
        }

    def _generate_inventory_output(self, data: dict, params: dict) -> dict:
        return {
            "type": "库存分析报告",
            "total_inventory": f"{data['total_inventory']:,}吨",
            "turnover_rate": data["turnover_rate"],
            "turnover_days": f"{data['turnover_days']}天",
            "slow_moving_ratio": f"{data['slow_moving_ratio']}%",
            "safety_stock": f"{data['safety_stock']:,}吨",
            "summary": f"总库存{data['total_inventory']:,}吨，周转率{data['turnover_rate']}次/年，呆滞率{data['slow_moving_ratio']}%",
        }

    def _generate_logistics_cost_output(self, data: dict, params: dict) -> dict:
        return {
            "type": "物流成本分析",
            "total_cost": f"¥{data['total_cost']:,.1f}万",
            "cost_per_ton": f"¥{data['cost_per_ton']}/吨",
            "industry_avg": f"¥{data['industry_avg']}/吨",
            "vs_industry": f"{data['vs_industry']}%（优于行业）" if data["vs_industry"] < 0 else f"+{data['vs_industry']}%（高于行业）",
            "breakdown": data["cost_breakdown"],
            "summary": f"物流成本¥{data['total_cost']:,.1f}万，单位成本¥{data['cost_per_ton']}/吨，{data['vs_industry']}% vs 行业",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "供应链数据已生成")
