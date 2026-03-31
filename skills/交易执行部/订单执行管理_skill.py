"""
订单执行管理 Skill - 交易执行部
订单全生命周期管理：从创建到关闭归档
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class OrderExecutionSkill(BaseSkill):
    """
    订单执行管理
    
    触发条件:
    - 用户说"订单执行"、"订单管理"
    - 用户说"订单状态"、"订单跟踪"
    - 用户说"订单关闭"、"订单归档"
    """

    name = "订单执行管理"
    description = "订单全生命周期管理，从创建到关闭归档"
    department = "交易执行部"
    
    trigger_keywords = [
        "订单执行", "订单管理", "订单状态",
        "订单跟踪", "订单关闭", "订单归档",
        "订单", "ORD",
    ]
    
    optional_keywords = [
        "查看", "跟踪", "关闭", "执行",
    ]
    
    examples = [
        "查看订单执行状态",
        "跟踪订单ORD-20260331-001",
        "关闭已完成订单",
    ]

    def parse_input(self, user_input: str) -> dict:
        params = {"sub_skill": "overview"}
        
        if re.search(r"跟踪|状态|查看", user_input):
            params["sub_skill"] = "tracking"
        elif re.search(r"关闭|归档", user_input):
            params["sub_skill"] = "close"
        
        order_no = re.search(r"ORD[_-]?\d+", user_input, re.IGNORECASE)
        if order_no:
            params["order_no"] = order_no.group()
        
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        return {
            "orders": [
                {"no": "ORD-20260331-001", "customer": "华东客户A", "product": "原油", "quantity": 5000, "status": "执行中", "progress": 60, "delivery_date": "2026-04-15"},
                {"no": "ORD-20260331-002", "customer": "华南客户B", "product": "燃料油", "quantity": 2000, "status": "待发运", "progress": 40, "delivery_date": "2026-04-20"},
                {"no": "ORD-20260328-001", "customer": "华北客户C", "product": "柴油", "quantity": 3000, "status": "已完成", "progress": 100, "delivery_date": "2026-03-28"},
            ]
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        orders = data["orders"]
        active = [o for o in orders if o["status"] not in ["已完成", "已关闭"]]
        completed = [o for o in orders if o["status"] in ["已完成", "已关闭"]]
        return {
            "type": "订单执行概览",
            "total": len(orders),
            "active": len(active),
            "completed": len(completed),
            "order_list": orders,
            "summary": f"共{len(orders)}笔订单，{len(active)}笔执行中，{len(completed)}笔已完成",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "订单数据已生成")
