"""
Finance Skill - 财务经营部综合技能入口
管理财务报表生成、发票结算、资金调度、预算执行监控等财务全流程业务
"""

import re
import asyncio
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class FinanceSkill(BaseSkill):
    """
    财务经营部综合技能
    
    触发条件:
    - 用户说"财务报表"、"月报"、"季报"、"年报"
    - 用户说"发票"、"结算"、"付款"
    - 用户说"资金"、"预算"、"执行率"
    """

    name = "财务经营部综合技能"
    description = "管理财务报表生成、发票结算、资金调度、预算执行监控等财务全流程业务"
    department = "财务经营部"
    
    trigger_keywords = [
        "财务报表", "财务报告", "月报", "季报", "年报",
        "发票", "结算", "付款",
        "资金", "预算", "执行率",
        "财务经营", "财务部",
    ]
    
    optional_keywords = [
        "生成", "查看", "分析", "监控",
    ]
    
    examples = [
        "生成本月财务报表",
        "查看发票结算情况",
        "资金调度建议",
        "预算执行率多少",
    ]

    def parse_input(self, user_input: str) -> dict:
        params = {
            "sub_skill": None,  # 报表/发票/资金/预算
            "period": None,      # 月报/季报/年报
            "date": None,
            "action": None,     # 生成/查看/分析
        }
        
        # 识别子技能
        if re.search(r"报表|月报|季报|年报", user_input):
            params["sub_skill"] = "report"
        elif re.search(r"发票|结算|付款", user_input):
            params["sub_skill"] = "invoice"
        elif re.search(r"资金|调度", user_input):
            params["sub_skill"] = "capital"
        elif re.search(r"预算|执行率", user_input):
            params["sub_skill"] = "budget"
        
        # 识别期间
        if re.search(r"本月|月报", user_input):
            params["period"] = "monthly"
        elif re.search(r"本季|季报", user_input):
            params["period"] = "quarterly"
        elif re.search(r"本年|年报", user_input):
            params["period"] = "yearly"
        
        # 识别动作
        if re.search(r"生成|制作|输出", user_input):
            params["action"] = "generate"
        elif re.search(r"查看|查询|看看", user_input):
            params["action"] = "view"
        elif re.search(r"分析|评估", user_input):
            params["action"] = "analyze"
        
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        """获取财务数据（预留API接口）"""
        await asyncio.sleep(0.2)
        
        sub_skill = params.get("sub_skill", "report")
        
        if sub_skill == "report":
            return self._mock_financial_report(params)
        elif sub_skill == "invoice":
            return self._mock_invoice_data(params)
        elif sub_skill == "capital":
            return self._mock_capital_data(params)
        elif sub_skill == "budget":
            return self._mock_budget_data(params)
        return {}

    def _mock_financial_report(self, params: dict) -> dict:
        return {
            "report_type": params.get("period", "monthly"),
            "period": datetime.now().strftime("%Y-%m"),
            "revenue": 12580.5,
            "gross_profit": 892.3,
            "gross_margin": 7.09,
            "net_profit": 356.2,
            "net_margin": 2.83,
            "assets": 45600.0,
            "liabilities": 32100.0,
            "equity": 13500.0,
            "debt_ratio": 70.39,
        }

    def _mock_invoice_data(self, params: dict) -> dict:
        return {
            "total_invoices": 156,
            "total_amount": 8920.5,
            "paid": 7230.8,
            "pending": 1689.7,
            "overdue": 0,
            "invoice_list": [
                {"no": "INV-20260331-001", "amount": 580.0, "status": "已付款"},
                {"no": "INV-20260331-002", "amount": 1260.5, "status": "待收款"},
                {"no": "INV-20260331-003", "amount": 890.0, "status": "已付款"},
            ]
        }

    def _mock_capital_data(self, params: dict) -> dict:
        return {
            "total_balance": 5680.5,
            "idle_funds": 1200.0,
            "occupied": 4480.5,
            "currency": "CNY",
            "suggestion": "建议将1200万闲置资金投入短期理财产品，预期年化收益2.5-3.5%",
        }

    def _mock_budget_data(self, params: dict) -> dict:
        return {
            "department": "全集团",
            "budget_amount": 15000.0,
            "executed": 8920.5,
            "execution_rate": 59.47,
            "status": "正常",
            "items": [
                {"item": "收入预算", "budget": 50000, "executed": 38500, "rate": 77.0},
                {"item": "成本预算", "budget": 42000, "executed": 32800, "rate": 78.1},
                {"item": "费用预算", "budget": 3000, "executed": 1890, "rate": 63.0},
            ]
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        sub_skill = params.get("sub_skill", "report")
        
        if sub_skill == "report":
            return self._generate_report_output(data, params)
        elif sub_skill == "invoice":
            return self._generate_invoice_output(data, params)
        elif sub_skill == "capital":
            return self._generate_capital_output(data, params)
        elif sub_skill == "budget":
            return self._generate_budget_output(data, params)
        return {"result": "无数据"}

    def _generate_report_output(self, data: dict, params: dict) -> dict:
        return {
            "report_type": "财务经营部报告",
            "period": data.get("period"),
            "revenue": f"¥{data['revenue']:,.1f}万元",
            "gross_profit": f"¥{data['gross_profit']:,.1f}万元",
            "gross_margin": f"{data['gross_margin']}%",
            "net_profit": f"¥{data['net_profit']:,.1f}万元",
            "net_margin": f"{data['net_margin']}%",
            "debt_ratio": f"{data['debt_ratio']}%",
            "summary": f"{data['period']}收入¥{data['revenue']:,.1f}万，毛利率{data['gross_margin']}%，净利润¥{data['net_profit']:,.1f}万",
        }

    def _generate_invoice_output(self, data: dict, params: dict) -> dict:
        return {
            "invoice_summary": f"共{data['total_invoices']}张发票，金额¥{data['total_amount']:,.1f}万",
            "paid": f"¥{data['paid']:,.1f}万",
            "pending": f"¥{data['pending']:,.1f}万",
            "overdue": f"¥{data['overdue']:,.1f}万",
            "summary": f"发票总额¥{data['total_amount']:,.1f}万，已收款¥{data['paid']:,.1f}万，{data['pending']:,.1f}万待收",
        }

    def _generate_capital_output(self, data: dict, params: dict) -> dict:
        return {
            "total_balance": f"¥{data['total_balance']:,.1f}万",
            "idle_funds": f"¥{data['idle_funds']:,.1f}万",
            "utilization_rate": f"{(1-data['idle_funds']/data['total_balance'])*100:.1f}%",
            "suggestion": data["suggestion"],
            "summary": f"资金余额¥{data['total_balance']:,.1f}万，闲置¥{data['idle_funds']:,.1f}万",
        }

    def _generate_budget_output(self, data: dict, params: dict) -> dict:
        return {
            "execution_rate": f"{data['execution_rate']}%",
            "status": data["status"],
            "executed": f"¥{data['executed']:,.1f}万",
            "budget": f"¥{data['budget_amount']:,.1f}万",
            "summary": f"预算执行率{data['execution_rate']}%，{data['status']}",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", f"财务数据已生成")
