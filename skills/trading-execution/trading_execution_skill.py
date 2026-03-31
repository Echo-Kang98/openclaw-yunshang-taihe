"""
TradingExecution Skill - 交易执行部综合技能
管理订单执行、单据管理、船务航次、物流协调
"""

import re
import asyncio
import random
from datetime import datetime, timedelta
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class TradingExecutionSkill(BaseSkill):
    """
    交易执行部综合技能
    
    触发条件:
    - 用户说"订单"、"执行"、"贸易执行"
    - 用户说"单据"、"提单"、"B/L"、"发票"
    - 用户说"船务"、"航次"、"租船"、"运费"
    - 用户说"物流"、"协调"、"到港"、"清关"
    """

    name = "交易执行部综合技能"
    description = "订单执行、单据管理、船务航次、物流协调"
    department = "交易执行部"
    
    trigger_keywords = [
        "订单", "执行", "贸易执行",
        "单据", "提单", "B/L", "发票",
        "船务", "航次", "租船", "运费",
        "物流", "协调", "到港", "清关",
        "交易执行部",
    ]
    
    optional_keywords = [
        "查看", "跟踪", "管理", "执行",
    ]
    
    examples = [
        "查看当前订单执行状态",
        "跟踪货物运输进度",
        "审核提单文件",
    ]

    def parse_input(self, user_input: str) -> dict:
        params = {"sub_skill": None}
        
        if re.search(r"订单", user_input):
            params["sub_skill"] = "order"
        elif re.search(r"单据|提单|B/L|发票", user_input):
            params["sub_skill"] = "document"
        elif re.search(r"船务|航次|租船|船", user_input):
            params["sub_skill"] = "shipping"
        elif re.search(r"物流|清关|到港|协调", user_input):
            params["sub_skill"] = "logistics"
        
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        sub_skill = params.get("sub_skill")
        
        if sub_skill == "order":
            return self._mock_order_data(params)
        elif sub_skill == "document":
            return self._mock_document_data(params)
        elif sub_skill == "shipping":
            return self._mock_shipping_data(params)
        return self._mock_logistics_data(params)

    def _mock_order_data(self, params: dict) -> dict:
        return {
            "orders": [
                {"no": "ORD-20260331-001", "customer": "华东客户A", "product": "原油", "quantity": 5000, "status": "执行中", "delivery_date": "2026-04-15"},
                {"no": "ORD-20260331-002", "customer": "华南客户B", "product": "燃料油", "quantity": 2000, "status": "待发运", "delivery_date": "2026-04-20"},
                {"no": "ORD-20260331-003", "customer": "华北客户C", "product": "柴油", "quantity": 3000, "status": "已完成", "delivery_date": "2026-03-28"},
            ],
            "total_orders": 3,
            "on_time_rate": 97.5,
        }

    def _mock_document_data(self, params: dict) -> dict:
        return {
            "documents": [
                {"type": "提单 B/L", "no": "BL-20260315-001", "status": "已签发", "date": "2026-03-15"},
                {"type": "发票 INV", "no": "INV-20260320-002", "status": "已开具", "date": "2026-03-20"},
                {"type": "装箱单 PL", "no": "PL-20260315-001", "status": "已归档", "date": "2026-03-15"},
                {"type": "产地证 CO", "no": "CO-20260318-001", "status": "审核中", "date": "2026-03-18"},
            ]
        }

    def _mock_shipping_data(self, params: dict) -> dict:
        return {
            "vessels": [
                {"name": "MV PEACE", "voyage": "V-2026-0315", "load_port": "Kuwait", "discharge_port": "Shanghai", "status": "航行中", "eta": "2026-04-10", "quantity": 45000},
                {"name": "MV HARMONY", "voyage": "V-2026-0320", "load_port": "Qatar", "discharge_port": "Ningbo", "status": "装港", "eta": "2026-04-18", "quantity": 38000},
            ],
            "freight_rates": {"sc_usd": 12.5, "brent_usd": 10.8, "wti_usd": 11.2},
        }

    def _mock_logistics_data(self, params: dict) -> dict:
        return {
            "shipments": [
                {"order_no": "ORD-20260331-001", "mode": "海运+陆运", "status": "清关中", "current_location": "上海港", "eta": "2026-04-15"},
                {"order_no": "ORD-20260331-002", "mode": "铁路", "status": "运输中", "current_location": "广州站", "eta": "2026-04-20"},
            ],
            "clearance_status": "正常",
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        sub_skill = params.get("sub_skill")
        
        if sub_skill == "order":
            return self._generate_order_output(data, params)
        elif sub_skill == "document":
            return self._generate_document_output(data, params)
        elif sub_skill == "shipping":
            return self._generate_shipping_output(data, params)
        return self._generate_logistics_output(data, params)

    def _generate_order_output(self, data: dict, params: dict) -> dict:
        orders = data["orders"]
        executing = sum(1 for o in orders if o["status"] == "执行中")
        return {
            "type": "订单执行概览",
            "total_orders": data["total_orders"],
            "executing": executing,
            "completed": sum(1 for o in orders if o["status"] == "已完成"),
            "on_time_rate": f"{data['on_time_rate']}%",
            "order_list": orders,
            "summary": f"共{data['total_orders']}笔订单，{executing}笔执行中，准时率{data['on_time_rate']}%",
        }

    def _generate_document_output(self, data: dict, params: dict) -> dict:
        docs = data["documents"]
        pending = sum(1 for d in docs if d["status"] in ["审核中", "待处理"])
        return {
            "type": "单据管理概览",
            "total_documents": len(docs),
            "pending": pending,
            "document_list": docs,
            "summary": f"共{len(docs)}份单据，{pending}份待处理",
        }

    def _generate_shipping_output(self, data: dict, params: dict) -> dict:
        vessels = data["vessels"]
        on_water = sum(1 for v in vessels if v["status"] == "航行中")
        return {
            "type": "船务航次概览",
            "total_vessels": len(vessels),
            "on_water": on_water,
            "at_port": sum(1 for v in vessels if v["status"] == "装港"),
            "vessel_list": vessels,
            "freight_rates": data["freight_rates"],
            "summary": f"共{len(vessels)}艘船，{on_water}艘航行中",
        }

    def _generate_logistics_output(self, data: dict, params: dict) -> dict:
        shipments = data["shipments"]
        return {
            "type": "物流协调概览",
            "total_shipments": len(shipments),
            "status_summary": {s["status"]: sum(1 for ss in shipments if ss["status"] == s["status"]) for s in shipments},
            "clearance_status": data["clearance_status"],
            "shipment_list": shipments,
            "summary": f"共{len(shipments)}票货物，整体{data['clearance_status']}",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "交易执行数据已生成")
