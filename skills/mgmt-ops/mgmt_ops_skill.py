"""
MgmtOps Skill - 卓越运营部综合技能
管理KPI监控看板、合规检查审计、效能分析报告、流程优化诊断
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class MgmtOpsSkill(BaseSkill):
    """
    卓越运营部综合技能
    
    触发条件:
    - 用户说"KPI"、"指标"、"达成率"
    - 用户说"合规"、"审计"、"检查"
    - 用户说"效能"、"效率"、"优化"
    - 用户说"流程"、"瓶颈"、"诊断"
    """

    name = "卓越运营部综合技能"
    description = "KPI监控看板、合规检查审计、效能分析报告、流程优化诊断"
    department = "卓越运营部"
    
    trigger_keywords = [
        "KPI", "指标", "达成率", "绩效",
        "合规", "审计", "检查",
        "效能", "效率", "优化",
        "流程", "瓶颈", "诊断",
        "卓越运营", "运营部",
    ]
    
    optional_keywords = [
        "查看", "分析", "报告", "监控",
    ]
    
    examples = [
        "查看本月KPI达成情况",
        "生成合规检查报告",
        "分析各部门效能",
        "诊断订单处理流程瓶颈",
    ]

    def parse_input(self, user_input: str) -> dict:
        params = {"sub_skill": None}
        
        if re.search(r"KPI|指标|达成", user_input):
            params["sub_skill"] = "kpi"
        elif re.search(r"合规|审计|检查", user_input):
            params["sub_skill"] = "compliance"
        elif re.search(r"效能|效率|分析", user_input):
            params["sub_skill"] = "efficiency"
        elif re.search(r"流程|瓶颈|优化|诊断", user_input):
            params["sub_skill"] = "process"
        
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        sub_skill = params.get("sub_skill")
        
        if sub_skill == "kpi":
            return self._mock_kpi_data(params)
        elif sub_skill == "compliance":
            return self._mock_compliance_data(params)
        elif sub_skill == "efficiency":
            return self._mock_efficiency_data(params)
        return self._mock_process_data(params)

    def _mock_kpi_data(self, params: dict) -> dict:
        return {
            "kpis": [
                {"name": "贸易量", "target": 50000, "actual": 46500, "rate": 93.0},
                {"name": "营业收入", "target": 10000, "actual": 8920, "rate": 89.2},
                {"name": "毛利率", "target": 5.0, "actual": 5.8, "rate": 116.0},
                {"name": "回款天数", "target": 45, "actual": 42, "rate": 95.6},
                {"name": "订单履约率", "target": 98, "actual": 97.5, "rate": 99.5},
            ]
        }

    def _mock_compliance_data(self, params: dict) -> dict:
        return {
            "check_type": "季度合规检查",
            "check_date": datetime.now().strftime("%Y-%m-%d"),
            "grade": "A",
            "total_items": 45,
            "passed_items": 43,
            "failed_items": 2,
            "failed_list": [
                {"item": "付款审批流程", "issue": "超权限付款1笔"},
                {"item": "合同用印", "issue": "部分合同未按要求盖章"},
            ]
        }

    def _mock_efficiency_data(self, params: dict) -> dict:
        return {
            "departments": [
                {"name": "贸易部", "score": 85.5, "trend": "上升"},
                {"name": "财务部", "score": 88.0, "trend": "稳定"},
                {"name": "物流部", "score": 72.3, "trend": "下降"},
                {"name": "风控部", "score": 91.2, "trend": "上升"},
            ],
            "overall_score": 84.3,
        }

    def _mock_process_data(self, params: dict) -> dict:
        return {
            "process_name": "订单处理流程",
            "total_duration_hours": 72,
            "bottleneck": {"环节": "财务审批", "耗时": 36, "占比": "50%"},
            "steps": [
                {"name": "订单录入", "duration": 2, "owner": "贸易部"},
                {"name": "风控审核", "duration": 8, "owner": "风控部"},
                {"name": "财务审批", "duration": 36, "owner": "财务部"},
                {"name": "执行发货", "duration": 20, "owner": "物流部"},
                {"name": "交付确认", "duration": 6, "owner": "贸易部"},
            ],
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        sub_skill = params.get("sub_skill")
        
        if sub_skill == "kpi":
            return self._generate_kpi_output(data, params)
        elif sub_skill == "compliance":
            return self._generate_compliance_output(data, params)
        elif sub_skill == "efficiency":
            return self._generate_efficiency_output(data, params)
        return self._generate_process_output(data, params)

    def _generate_kpi_output(self, data: dict, params: dict) -> dict:
        kpis = data["kpis"]
        on_target = sum(1 for k in kpis if k["rate"] >= 100)
        return {
            "type": "KPI监控看板",
            "total_kpis": len(kpis),
            "on_target": on_target,
            "overall_rate": round(sum(k["rate"] for k in kpis) / len(kpis), 1),
            "kpi_list": kpis,
            "summary": f"KPI共{len(kpis)}项，{on_target}项达标，整体达成率{sum(k['rate'] for k in kpis)/len(kpis):.1f}%",
        }

    def _generate_compliance_output(self, data: dict, params: dict) -> dict:
        return {
            "type": "合规检查报告",
            "grade": data["grade"],
            "passed_items": f"{data['passed_items']}/{data['total_items']}",
            "failed_count": data["failed_items"],
            "failed_list": data["failed_list"],
            "summary": f"合规评级{data['grade']}级，通过{data['passed_items']}/{data['total_items']}项，发现{data['failed_items']}项不符合",
        }

    def _generate_efficiency_output(self, data: dict, params: dict) -> dict:
        return {
            "type": "效能分析报告",
            "overall_score": data["overall_score"],
            "departments": data["departments"],
            "lowest_dept": min(data["departments"], key=lambda d: d["score"])["name"],
            "summary": f"集团效能综合得分{data['overall_score']}，{data['departments'][0]['name']}最优，{min(data['departments'], key=lambda d:d['score'])['name']}最低",
        }

    def _generate_process_output(self, data: dict, params: dict) -> dict:
        bottleneck = data["bottleneck"]
        return {
            "type": "流程优化诊断报告",
            "process_name": data["process_name"],
            "total_duration": f"{data['total_duration_hours']}小时",
            "bottleneck": f"{bottleneck['环节']}（占比{bottleneck['占比']}）",
            "suggestion": f"建议优化{bottleneck['环节']}，可缩短整体处理时长30-40%",
            "summary": f"订单处理流程总耗时{data['total_duration_hours']}小时，瓶颈在{bottleneck['环节']}",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "运营数据已生成")
