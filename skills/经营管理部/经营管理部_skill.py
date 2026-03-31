"""
Management Skill - 经营管理部综合技能
战略规划支持、竞争对手分析、经营分析报告、经营风险预警、绩效考核管理
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class ManagementSkill(BaseSkill):
    """
    经营管理部综合技能
    
    触发条件:
    - 用户说"战略"、"规划"、"布局"
    - 用户说"竞争对手"、"竞争分析"
    - 用户说"经营分析"、"经营报告"
    - 用户说"风险预警"、"预警"
    - 用户说"绩效考核"、"KPI考核"
    """

    name = "经营管理部综合技能"
    description = "战略规划、竞争对手分析、经营分析报告、风险预警、绩效考核"
    department = "经营管理部"
    
    trigger_keywords = [
        "战略", "规划", "布局",
        "竞争对手", "竞争分析",
        "经营分析", "经营报告", "月报",
        "风险预警", "预警",
        "绩效考核", "KPI考核",
        "经营管理",
    ]
    
    optional_keywords = [
        "分析", "查看", "生成", "管理",
    ]
    
    examples = [
        "生成月度经营分析报告",
        "分析主要竞争对手动态",
        "战略规划建议",
        "本月风险预警",
    ]

    def parse_input(self, user_input: str) -> dict:
        params = {"sub_skill": None}
        
        if re.search(r"战略|规划", user_input):
            params["sub_skill"] = "strategy"
        elif re.search(r"竞争对手|竞争", user_input):
            params["sub_skill"] = "competitor"
        elif re.search(r"经营分析|经营报告", user_input):
            params["sub_skill"] = "business_analysis"
        elif re.search(r"风险预警|预警", user_input):
            params["sub_skill"] = "risk_warning"
        elif re.search(r"绩效考核|KPI考核", user_input):
            params["sub_skill"] = "performance"
        
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        sub_skill = params.get("sub_skill")
        
        if sub_skill == "strategy":
            return self._mock_strategy_data(params)
        elif sub_skill == "competitor":
            return self._mock_competitor_data(params)
        elif sub_skill == "business_analysis":
            return self._mock_business_data(params)
        elif sub_skill == "risk_warning":
            return self._mock_risk_data(params)
        return self._mock_performance_data(params)

    def _mock_strategy_data(self, params: dict) -> dict:
        return {
            "market_size": 12000,
            "our_share": 8.5,
            "growth_rate": 12.5,
            "opportunities": ["新能源配套", "进口替代"],
            "threats": ["竞争对手价格战", "政策变化"],
        }

    def _mock_competitor_data(self, params: dict) -> dict:
        return {
            "competitors": [
                {"name": "中石化", "market_share": 25, "strength": "规模大，渠道广", "weakness": "价格偏高"},
                {"name": "振华石油", "market_share": 12, "strength": "价格灵活", "weakness": "品质不稳"},
            ]
        }

    def _mock_business_data(self, params: dict) -> dict:
        return {
            "revenue": 12580,
            "gross_profit": 892,
            "net_profit": 356,
            "budget_rate": 78.5,
            "vs_last_month": 5.2,
        }

    def _mock_risk_data(self, params: dict) -> dict:
        return {
            "risks": [
                {"type": "市场风险", "level": "🟡", "desc": "原油价格波动加剧", "suggestion": "加强套保"},
                {"type": "信用风险", "level": "🟢", "desc": "客户信用良好", "suggestion": "维持现状"},
            ]
        }

    def _mock_performance_data(self, params: dict) -> dict:
        return {
            "departments": [
                {"name": "贸易部", "score": 85, "level": "B+"},
                {"name": "财务部", "score": 88, "level": "B+"},
                {"name": "物流部", "score": 72, "level": "C"},
            ]
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        sub_skill = params.get("sub_skill")
        
        if sub_skill == "strategy":
            return {"type": "战略规划", "data": data, "summary": "战略规划建议已生成"}
        elif sub_skill == "competitor":
            return {"type": "竞争对手分析", "competitors": data["competitors"], "summary": f"监测{len(data['competitors'])}个竞争对手"}
        elif sub_skill == "business_analysis":
            return {"type": "经营分析报告", "revenue": f"¥{data['revenue']}万", "budget_rate": f"{data['budget_rate']}%", "summary": f"收入¥{data['revenue']}万，预算完成率{data['budget_rate']}%"}
        elif sub_skill == "risk_warning":
            return {"type": "风险预警", "risks": data["risks"], "summary": f"监测到{len(data['risks'])}项风险"}
        return {"type": "绩效考核", "departments": data["departments"], "summary": f"共{len(data['departments'])}个部门参与考核"}

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "经营管理数据已生成")
