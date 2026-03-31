"""
物流协调管理 Skill - 交易执行部
协调多式联运、时效管理、异常处理、物流成本控制
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class LogisticsCoordinationSkill(BaseSkill):
    """
    物流协调管理
    
    触发条件:
    - 用户说"物流协调"、"多式联运"
    - 用户说"时效"、"延误"、"跟踪"
    - 用户说"异常处理"、"滞箱"、"滞港"
    - 用户说"物流成本"、"运费优化"
    """

    name = "物流协调管理"
    description = "协调多式联运、时效管理、异常处理、物流成本控制"
    department = "交易执行部"
    
    trigger_keywords = [
        "物流协调", "多式联运", "时效管理",
        "延误", "跟踪", "异常",
        "滞箱", "滞港", "货损",
        "物流成本", "运费优化", "降本",
        "物流", "运输",
    ]
    
    optional_keywords = [
        "分析", "查看", "处理", "优化", "协调",
    ]
    
    examples = [
        "查看物流时效情况",
        "处理滞箱异常",
        "分析物流成本",
    ]

    def parse_input(self, user_input: str) -> dict:
        params = {"sub_skill": None}
        
        if re.search(r"时效|跟踪|进度", user_input):
            params["sub_skill"] = "tracking"
        elif re.search(r"异常|延误|滞箱|滞港|货损", user_input):
            params["sub_skill"] = "exception"
        elif re.search(r"成本|运费|降本|优化", user_input):
            params["sub_skill"] = "cost"
        else:
            params["sub_skill"] = "overview"
        
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        
        if params.get("sub_skill") == "tracking":
            return self._mock_tracking_data(params)
        elif params.get("sub_skill") == "exception":
            return self._mock_exception_data(params)
        elif params.get("sub_skill") == "cost":
            return self._mock_cost_data(params)
        return self._mock_overview_data(params)

    def _mock_overview_data(self, params: dict) -> dict:
        return {
            "total_shipments": 8,
            "on_time_rate": 87.5,
            "active_alerts": 2,
            "cost_summary": {"total": 285, "per_ton": 28.5},
        }

    def _mock_tracking_data(self, params: dict) -> dict:
        return {
            "shipments": [
                {"no": "SHP-001", "route": " Kuwait → 上海", "mode": "海运", "status": "航行中", "progress": 65, "eta": "2026-04-10"},
                {"no": "SHP-002", "route": " Qatar → 宁波", "mode": "海运", "status": "装港", "progress": 20, "eta": "2026-04-18"},
            ]
        }

    def _mock_exception_data(self, params: dict) -> dict:
        return {
            "exceptions": [
                {"type": "滞箱", "shipment": "SHP-001", "desc": "上海港箱子紧张，预计延误2天", "level": "🟡", "action": "已协调优先提箱"},
                {"type": "查验", "shipment": "SHP-002", "desc": "海关随机查验", "level": "🟠", "action": "配合查验，准备补充资料"},
            ]
        }

    def _mock_cost_data(self, params: dict) -> dict:
        return {
            "total_cost": 285.0,
            "cost_breakdown": {"海运费": 142, "陆运费": 57, "仓储": 43, "清关": 28, "其他": 15},
            "per_ton": 28.5,
            "industry_avg": 32.0,
            "saving_opportunity": 15.0,
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        sub_skill = params.get("sub_skill")
        
        if sub_skill == "tracking":
            return {"type": "物流跟踪", "shipments": data["shipments"], "summary": f"共{len(data['shipments'])}票货物"}
        elif sub_skill == "exception":
            return {"type": "异常处理", "exceptions": data["exceptions"], "summary": f"共{len(data['exceptions'])}项异常"}
        elif sub_skill == "cost":
            return {"type": "物流成本分析", "cost": f"¥{data['total_cost']}万", "per_ton": f"¥{data['per_ton']}/吨", "saving": f"可节省¥{data['saving_opportunity']}万", "summary": f"物流成本¥{data['total_cost']}万/吨"}
        return {"type": "物流协调概览", "total": data["total_shipments"], "on_time": f"{data['on_time_rate']}%", "summary": f"共{data['total_shipments']}票，准时率{data['on_time_rate']}%"}

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "物流数据已生成")
