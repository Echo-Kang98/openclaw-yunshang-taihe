"""
财务报表生成 Skill
自动汇总业务数据，生成符合会计准则的财务报表（P&L、资产负债表、现金流量表）

输入: 月份/季度/年度
输出: JSON格式报表
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat
from tools.formatters import format_currency, format_percentage


class FinancialReportSkill(BaseSkill):
    """
    财务报表生成Skill
    
    触发条件:
    - 财务人员说"生成月度财务报表"
    - 高管要求"看看本月P&L"
    - 审计/监管需要的定期报告
    
    执行步骤:
    1. 从各业务系统拉取本月贸易成交记录
    2. 获取采购成本、销售收入、仓储物流费用等成本数据
    3. 获取外汇兑换记录和汇兑损益数据
    4. 获取资金利息收支数据
    5. 按会计准则计算各项指标
    6. 生成三表（利润表、资产负债表、现金流量表）
    """

    name = "财务报表生成"
    description = "自动汇总业务数据，生成符合会计准则的财务报表"
    department = "财务经营部"
    
    trigger_keywords = [
        "财务报表", "财务报告", "月度报表", "季度报告", "年度报告",
        "P&L", "利润表", "资产负债表", "现金流量表",
        "生成报表", "看看本月", "本月营收", "本月利润",
    ]
    
    optional_keywords = [
        "生成", "看看", "查看", "查询", "本月", "本月度", "本季度", "本年",
    ]
    
    examples = [
        "生成2026年1月财务报表",
        "看看本月P&L",
        "查询季度财务报告",
    ]

    def parse_input(self, user_input: str) -> dict:
        """
        解析用户输入，提取报表期间和类型
        
        支持格式:
        - "生成2026年1月财务报表" -> period="2026-01", type="monthly"
        - "看看本月P&L" -> period="current", type="monthly"
        - "查询季度财务报告" -> period="current", type="quarterly"
        - "2026年Q1报告" -> period="2026-Q1", type="quarterly"
        """
        params = {"period": None, "report_type": "monthly", "year": None, "month": None}
        
        # 提取年份
        year_match = re.search(r"20\d{2}年?", user_input)
        if year_match:
            params["year"] = re.sub(r"年", "", year_match.group())
        
        # 提取月份
        month_match = re.search(r"(\d+)月", user_input)
        if month_match:
            params["month"] = int(month_match.group(1))
            params["report_type"] = "monthly"
        
        # 提取季度
        quarter_match = re.search(r"Q([1-4])", user_input, re.IGNORECASE)
        if quarter_match:
            params["quarter"] = int(quarter_match.group(1))
            params["report_type"] = "quarterly"
        
        # 判断报告类型
        if any(kw in user_input for kw in ["季度", "Q1", "Q2", "Q3", "Q4"]):
            params["report_type"] = "quarterly"
        elif any(kw in user_input for kw in ["年度", "年报", "全年"]):
            params["report_type"] = "annual"
        
        # 确定期间
        if params["year"] and params.get("month"):
            params["period"] = f"{params['year']}-{params['month']:02d}"
        elif params["year"] and params.get("quarter"):
            params["period"] = f"{params['year']}-Q{params['quarter']}"
        elif params["year"]:
            params["period"] = params["year"]
        else:
            # 默认当前月份
            now = datetime.now()
            params["year"] = str(now.year)
            params["month"] = now.month
            params["period"] = now.strftime("%Y-%m")
        
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        """
        获取财务报表所需数据
        
        TODO: 接入真实数据源
        - 交易执行部_订单成交明细
        - 财务经营部_资金流水
        - 汇率经营部_汇兑损益台账
        
        目前使用模拟数据
        """
        await asyncio.sleep(0.2)  # 模拟API延迟
        
        period = params.get("period", datetime.now().strftime("%Y-%m"))
        report_type = params.get("report_type", "monthly")
        
        # 模拟基础数据
        base_revenue = random.uniform(2.5, 4.5)  # 亿元
        gross_margin = random.uniform(0.12, 0.22)  # 毛利率
        
        return {
            "period": period,
            "report_type": report_type,
            "generated_at": datetime.now().isoformat(),
            
            # 收入数据
            "revenue": {
                "total": round(base_revenue * 10000, 2),  # 万元
                "crude_oil_trade": round(base_revenue * 10000 * 0.65, 2),
                "chemical_trade": round(base_revenue * 10000 * 0.25, 2),
                "other_trade": round(base_revenue * 10000 * 0.10, 2),
            },
            
            # 成本数据
            "cost": {
                "total": round(base_revenue * 10000 * (1 - gross_margin), 2),
                "procurement_cost": round(base_revenue * 10000 * 0.55, 2),
                "logistics_cost": round(base_revenue * 10000 * 0.08, 2),
                "storage_cost": round(base_revenue * 10000 * 0.03, 2),
            },
            
            # 毛利
            "gross_profit": round(base_revenue * 10000 * gross_margin, 2),
            "gross_margin": round(gross_margin * 100, 2),
            
            # 费用
            "expenses": {
                "total": round(base_revenue * 10000 * random.uniform(0.04, 0.08), 2),
                "management": round(base_revenue * 10000 * 0.02, 2),
                "financial": round(base_revenue * 10000 * 0.015, 2),
                "sales": round(base_revenue * 10000 * 0.01, 2),
            },
            
            # 汇兑损益
            "fx_gain_loss": round(random.uniform(-500, 800), 2),
            
            # 净利润
            "net_profit": round(base_revenue * 10000 * gross_margin * random.uniform(0.6, 0.8), 2),
            
            # 资产负债表摘要
            "balance_sheet": {
                "current_assets": round(base_revenue * 10000 * 2.5, 2),
                "accounts_receivable": round(base_revenue * 10000 * 0.8, 2),
                "inventory": round(base_revenue * 10000 * 0.6, 2),
                "current_liabilities": round(base_revenue * 10000 * 1.5, 2),
                "accounts_payable": round(base_revenue * 10000 * 0.5, 2),
            },
            
            # 现金流量表摘要
            "cash_flow": {
                "operating": round(base_revenue * 10000 * random.uniform(0.1, 0.3), 2),
                "investing": round(random.uniform(-200, -50), 2),
                "financing": round(random.uniform(-100, 100), 2),
            },
            
            # 运营指标
            "kpis": {
                "ar_days": round(random.uniform(25, 35), 1),  # 应收账款周转天数
                "inventory_days": round(random.uniform(20, 30), 1),
                "ap_days": round(random.uniform(30, 45), 1),
            },
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        """
        生成标准化财务报表输出
        """
        period = data.get("period", "")
        period_display = self._format_period_display(period, data.get("report_type", "monthly"))
        
        # 利润表
        income_statement = {
            "period": period_display,
            "prepared_date": datetime.now().strftime("%Y-%m-%d"),
            "currency_unit": "人民币万元",
            "items": {
                "营业收入": data["revenue"]["total"],
                "其中：原油贸易": data["revenue"]["crude_oil_trade"],
                "其中：化工品": data["revenue"]["chemical_trade"],
                "其中：其他": data["revenue"]["other_trade"],
                "营业成本": data["cost"]["total"],
                "毛利": data["gross_profit"],
                "毛利率": f"{data['gross_margin']}%",
                "期间费用": data["expenses"]["total"],
                "汇兑损益": data["fx_gain_loss"],
                "净利润": data["net_profit"],
            }
        }
        
        # 资产负债表
        balance_sheet = {
            "流动资产合计": data["balance_sheet"]["current_assets"],
            "应收账款": data["balance_sheet"]["accounts_receivable"],
            "存货": data["balance_sheet"]["inventory"],
            "流动负债合计": data["balance_sheet"]["current_liabilities"],
            "应付账款": data["balance_sheet"]["accounts_payable"],
        }
        
        # 现金流量表
        cash_flow = {
            "经营活动现金流": data["cash_flow"]["operating"],
            "投资活动现金流": data["cash_flow"]["investing"],
            "筹资活动现金流": data["cash_flow"]["financing"],
            "现金净增加额": sum(data["cash_flow"].values()),
        }
        
        return {
            "report_type": "财务报表",
            "company_name": "泰和嘉柏",
            "period": period_display,
            "prepared_date": datetime.now().strftime("%Y-%m-%d"),
            "currency_unit": "人民币万元",
            "income_statement": income_statement,
            "balance_sheet": balance_sheet,
            "cash_flow": cash_flow,
            "kpis": data["kpis"],
            "summary": f"{period_display}营收{data['revenue']['total']/10000:.1f}亿元，净利润{data['net_profit']/10000:.1f}亿元，毛利率{data['gross_margin']}%，应收账款周转天数{data['kpis']['ar_days']}天",
        }

    def _format_period_display(self, period: str, report_type: str) -> str:
        """格式化期间显示"""
        if report_type == "monthly" and "-" in period:
            year, month = period.split("-")
            return f"{year}年{month}月"
        elif report_type == "quarterly" and "-Q" in period:
            year, q = period.split("-Q")
            return f"{year}年第{q}季度"
        elif report_type == "annual":
            return f"{period}年度"
        return period

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        """生成一句话摘要"""
        revenue_wan = data["revenue"]["total"]
        net_profit_wan = data["net_profit"]
        gross_margin = data["gross_margin"]
        ar_days = data["kpis"]["ar_days"]
        period_display = output.get("period", "")
        
        return f"{period_display}营收{revenue_wan/10000:.1f}亿元，净利润{net_profit_wan/10000:.1f}亿元，毛利率{gross_margin}%，应收账款周转天数{ar_days}天"


# ============ 使用示例 ============

async def main():
    """使用示例"""
    skill = FinancialReportSkill()
    
    test_inputs = [
        "生成2026年1月财务报表",
        "看看本月P&L",
        "查询2026年Q1季度报告",
    ]
    
    for user_input in test_inputs:
        print(f"\n{'='*60}")
        print(f"输入: {user_input}")
        print(f"can_handle: {skill.can_handle(user_input)}")
        
        params = skill.parse_input(user_input)
        print(f"解析参数: {params}")
        
        context = {"user_input": user_input}
        result = await skill.execute(context)
        
        print(f"\n执行结果:")
        print(f"  success: {result.success}")
        print(f"  skill_name: {result.skill_name}")
        print(f"  execution_time_ms: {result.execution_time_ms:.2f}ms")
        print(f"\n输出数据:")
        print(f"  营收: {result.data['income_statement']['items']['营业收入']:,.2f}万元")
        print(f"  净利润: {result.data['income_statement']['items']['净利润']:,.2f}万元")
        print(f"  毛利率: {result.data['income_statement']['items']['毛利率']}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
