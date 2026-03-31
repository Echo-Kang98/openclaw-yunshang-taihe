"""
船务与航次管理 Skill - 交易执行部
租船订舱、航次跟踪、运费结算、港口协调
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class ShippingVoyageSkill(BaseSkill):
    """
    船务与航次管理
    
    触发条件:
    - 用户说"船务"、"航次"、"租船"
    - 用户说"订舱"、"舱位"、"受载期"
    - 用户说"运费"、"BAF"、"PSS"
    - 用户说"装港"、"卸港"、"到港"
    """

    name = "船务与航次管理"
    description = "租船订舱、航次跟踪、运费结算、港口协调"
    department = "交易执行部"
    
    trigger_keywords = [
        "船务", "航次", "租船", "订舱",
        "运费", "BAF", "PSS", "港口拥挤费",
        "装港", "卸港", "到港", "离港",
        "航次管理", "船务管理",
    ]
    
    optional_keywords = [
        "查询", "跟踪", "结算", "安排",
    ]
    
    examples = [
        "查看在途航次",
        "查询运费报价",
        "跟踪装港进度",
    ]

    def parse_input(self, user_input: str) -> dict:
        params = {"sub_skill": None}
        
        if re.search(r"订舱|租船|舱位", user_input):
            params["sub_skill"] = "booking"
        elif re.search(r"航次|装港|卸港|到港", user_input):
            params["sub_skill"] = "voyage"
        elif re.search(r"运费|报价|结算", user_input):
            params["sub_skill"] = "freight"
        else:
            params["sub_skill"] = "overview"
        
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        
        if params.get("sub_skill") == "booking":
            return self._mock_booking_data(params)
        elif params.get("sub_skill") == "voyage":
            return self._mock_voyage_data(params)
        elif params.get("sub_skill") == "freight":
            return self._mock_freight_data(params)
        return self._mock_overview_data(params)

    def _mock_overview_data(self, params: dict) -> dict:
        return {
            "vessels": [
                {"name": "MV PEACE", "voyage": "V-2026-0315", "status": "航行中", "load": "Kuwait", "discharge": "上海", "eta": "2026-04-10"},
                {"name": "MV HARMONY", "voyage": "V-2026-0320", "status": "装港", "load": "Qatar", "discharge": "宁波", "eta": "2026-04-18"},
            ]
        }

    def _mock_booking_data(self, params: dict) -> dict:
        return {
            "available_space": [
                {"port": "上海", "vessel": "MV GLORY", "eta": "2026-04-15", "space": 5000, "freight": 12.5},
                {"port": "宁波", "vessel": "MV FORTUNE", "eta": "2026-04-20", "space": 3000, "freight": 11.8},
            ]
        }

    def _mock_voyage_data(self, params: dict) -> dict:
        return {
            "voyages": [
                {"name": "MV PEACE", "voyage": "V-2026-0315", "stage": "航行中", "progress": 65, "load_port": "Kuwait", "discharge_port": "上海", "eta": "2026-04-10 08:00"},
            ]
        }

    def _mock_freight_data(self, params: dict) -> dict:
        return {
            "routes": [
                {"route": "Kuwait → 上海", "base_freight": 12.5, "baf": 2.8, "pss": 1.5, "total": 16.8, "unit": "USD/桶"},
                {"route": "Qatar → 宁波", "base_freight": 11.8, "baf": 2.5, "pss": 1.2, "total": 15.5, "unit": "USD/桶"},
            ]
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        sub_skill = params.get("sub_skill")
        
        if sub_skill == "booking":
            return {"type": "订舱查询", "available": data["available_space"], "summary": f"当前有{len(data['available_space'])}个舱位可用"}
        elif sub_skill == "voyage":
            return {"type": "航次跟踪", "voyages": data["voyages"], "summary": f"共{len(data['voyages'])}个航次"}
        elif sub_skill == "freight":
            return {"type": "运费报价", "routes": data["routes"], "summary": f"共{len(data['routes'])}条航线运价"}
        return {"type": "船务概览", "vessels": data["vessels"], "summary": f"共{len(data['vessels'])}艘船在途"}

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "船务数据已生成")
