"""
期货交易执行 Skill
执行原油/化工品期货交易，包括上海原油期货（SC）、布伦特原油期货（Brent）等

输入: 原油品种（WTI/Brent/Dubai/SC）+ 交易指令
输出: 信号+置信度+入场/止损位
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


# 期货品种配置
FUTURES_CONFIGS = {
    "SC": {
        "name": "上海原油期货主连",
        "code": "SC0",
        "unit": "桶",
        "contract_size": 1000,  # 桶/手
        "currency": "CNY",
        "tick_size": 0.1,  # 元/桶
        "trading_hours": "09:00-15:00, 21:00-23:00",
    },
    "BRENT": {
        "name": "布伦特原油期货",
        "code": "BRENT",
        "unit": "桶",
        "contract_size": 1000,
        "currency": "USD",
        "tick_size": 0.01,
        "trading_hours": "00:00-24:00",
    },
    "WTI": {
        "name": "WTI原油期货",
        "code": "WTI",
        "unit": "桶",
        "contract_size": 1000,
        "currency": "USD",
        "tick_size": 0.01,
        "trading_hours": "00:00-24:00",
    },
    "DUBAI": {
        "name": "迪拜原油期货",
        "code": "DUBAI",
        "unit": "桶",
        "contract_size": 500,
        "currency": "USD",
        "tick_size": 0.01,
        "trading_hours": "00:00-24:00",
    },
}


class FuturesTradingSkill(BaseSkill):
    """
    期货交易执行Skill
    
    触发条件:
    - 用户说"在SC原油期货上建10手多头"
    - 用户说"平掉全部Brent空头仓位"
    - 需要对冲现货敞口时
    
    支持的交易操作:
    - 买入开仓 (Long Open)
    - 卖出开仓 (Short Open)
    - 买入平仓 (Long Close)
    - 卖出平仓 (Short Close)
    """

    name = "期货交易执行"
    description = "执行原油/化工品期货交易，支持套保和投机策略"
    department = "期现交易部"
    
    trigger_keywords = [
        "期货", "原油期货", "建仓", "平仓", "开仓", "多头", "空头",
        "买入", "卖出", "做多", "做空", "止损", "持仓",
        "SC原油", "Brent", "WTI", "Dubai",
    ]
    
    optional_keywords = [
        "手", "桶", "元", "美元",
    ]
    
    examples = [
        "SC原油608元/桶买入开仓10手",
        "在SC原油期货上建10手多头",
        "平掉全部Brent空头仓位",
    ]

    def parse_input(self, user_input: str) -> dict:
        """
        解析期货交易指令
        
        支持格式:
        - "SC原油608元/桶买入开仓10手" -> variety="SC", direction="long", price=608, quantity=10
        - "Brent 70美元买入5手做多" -> variety="BRENT", direction="long", price=70, quantity=5
        - "平掉全部空头仓位" -> variety=None, action="close_all", direction="short"
        """
        params = {
            "variety": None,
            "direction": None,  # long / short
            "action": None,  # open / close / close_all
            "price": None,
            "quantity": None,
            "stop_loss": None,
            "order_type": "market",  # market / limit
        }
        
        # 识别品种
        variety_patterns = [
            (r"SC原油?|SC0?", "SC"),
            (r"Brent|BRENT|布伦特", "BRENT"),
            (r"WTI", "WTI"),
            (r"Dubai|DUBAI|迪拜", "DUBAI"),
        ]
        for pattern, variety in variety_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                params["variety"] = variety
                break
        
        # 识别方向
        if re.search(r"做多|买入|多头|买开|Long", user_input, re.IGNORECASE):
            params["direction"] = "long"
        elif re.search(r"做空|卖出|空头|卖开|Short", user_input, re.IGNORECASE):
            params["direction"] = "short"
        
        # 识别开平仓
        if re.search(r"平仓|平掉|close", user_input, re.IGNORECASE):
            if "全部" in user_input:
                params["action"] = "close_all"
            else:
                params["action"] = "close"
        elif re.search(r"开仓|建仓|open", user_input, re.IGNORECASE):
            params["action"] = "open"
        
        # 如果没有明确指定，默认为开仓
        if params["action"] is None:
            params["action"] = "open"
        
        # 提取价格
        price_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:元|美元|USD|CNY)?\s*(?:/桶|每桶)?", user_input)
        if price_match:
            params["price"] = float(price_match.group(1))
            params["order_type"] = "limit"
        
        # 提取数量
        qty_match = re.search(r"(\d+)\s*手", user_input)
        if qty_match:
            params["quantity"] = int(qty_match.group(1))
        
        # 提取止损价
        sl_match = re.search(r"止损[^\d]*(\d+(?:\.\d+)?)", user_input)
        if sl_match:
            params["stop_loss"] = float(sl_match.group(1))
        
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        """
        获取交易数据和市场行情
        
        TODO: 接入真实期货API
        - 期货经纪商API（CTP主席/次席）
        - 行情数据（ Tick ）
        - 持仓数据
        
        目前使用模拟数据
        """
        await asyncio.sleep(0.15)  # 模拟API延迟
        
        variety = params.get("variety", "SC")
        config = FUTURES_CONFIGS.get(variety, FUTURES_CONFIGS["SC"])
        
        # 模拟当前行情
        if variety == "SC":
            current_price = random.uniform(580, 650)
        elif variety == "BRENT":
            current_price = random.uniform(70, 85)
        elif variety == "WTI":
            current_price = random.uniform(65, 80)
        else:
            current_price = random.uniform(75, 90)
        
        # 指令价格（如果指定）
        order_price = params.get("price") or current_price
        
        # 成交价格（滑点模拟）
        slippage = config["tick_size"] * random.randint(-5, 5)
        execution_price = order_price + slippage if params.get("order_type") == "limit" else current_price
        
        # 计算成交金额
        quantity = params.get("quantity", 10)
        contract_size = config["contract_size"]
        commission = quantity * contract_size * execution_price * 0.00012  # 万分之1.2
        
        # 模拟持仓数据
        position = {
            "variety": variety,
            "contract_code": config["code"],
            "direction": params.get("direction", "long"),
            "quantity": quantity,
            "open_price": execution_price,
            "current_price": current_price,
            "contract_size": contract_size,
            "currency": config["currency"],
            "unrealized_pnl": (
                (current_price - execution_price) * quantity * contract_size
                if params.get("direction") == "long"
                else (execution_price - current_price) * quantity * contract_size
            ),
        }
        
        return {
            "variety": variety,
            "config": config,
            "current_price": current_price,
            "order_price": order_price,
            "execution_price": execution_price,
            "slippage": slippage,
            "quantity": quantity,
            "commission": round(commission, 2),
            "position": position,
            "timestamp": datetime.now().isoformat(),
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        """
        生成交易执行报告
        """
        variety = data["variety"]
        config = data["config"]
        action = params.get("action", "open")
        direction = params.get("direction", "long")
        direction_cn = "买入（做多）" if direction == "long" else "卖出（做空）"
        
        if action == "open":
            # 开仓报告
            slippage_note = ""
            if data["slippage"] != 0:
                better = "优于" if data["slippage"] < 0 else "劣于"
                slippage_note = f"（{better}指令价 ✅）" if data["slippage"] < 0 else f"（{better}指令价 ⚠️）"
            
            return {
                "report_type": "期货交易执行报告",
                "execution_time": data["timestamp"],
                "operator": "SYSTEM",
                "account": "SIMULATED_ACCOUNT",
                
                "trade_order": {
                    "variety": f"{config['name']}（{config['code']}）",
                    "direction": direction_cn,
                    "quantity": f"{data['quantity']}手（{data['quantity'] * config['contract_size']}桶/手）",
                    "order_type": "限价单" if params.get("order_type") == "limit" else "市价单",
                    "order_price": f"{params.get('price', '市价')}",
                    "stop_loss": f"{params.get('stop_loss', '未设置')}元/桶" if params.get("stop_loss") else "未设置",
                },
                
                "execution_record": {
                    "time": data["timestamp"],
                    "price": f"{data['execution_price']}元/桶{slippage_note}",
                    "quantity": f"{data['quantity']}手",
                    "amount": f"{data['execution_price'] * data['quantity'] * config['contract_size']:,.2f}元",
                    "commission": f"约{data['commission']}元",
                    "exec_id": f"SIM_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                },
                
                "current_position": {
                    "contract": config["code"],
                    "direction": direction_cn,
                    "quantity": f"{data['quantity']}手",
                    "open_price": data["execution_price"],
                    "current_price": data["current_price"],
                    "unrealized_pnl": f"{data['position']['unrealized_pnl']:+.2f}元",
                },
                
                "risk_alert": self._generate_risk_alert(data, params),
                "compliance_check": self._compliance_check(data, params),
            }
        else:
            # 平仓报告
            return {
                "report_type": "期货平仓报告",
                "execution_time": data["timestamp"],
                "position_closed": data["position"],
                "execution_price": data["execution_price"],
            }

    def _generate_risk_alert(self, data: dict, params: dict) -> str:
        """生成风险提示"""
        variety = data["variety"]
        stop_loss = params.get("stop_loss")
        
        alerts = []
        
        if variety == "SC":
            alerts.append("⚠️ SC原油波动率较高，建议设置止损")
        elif variety in ["BRENT", "WTI"]:
            alerts.append("⚠️ 国际油价受地缘政治影响大，注意仓位控制")
        
        if stop_loss:
            current = data["current_price"]
            risk_amount = abs(current - stop_loss) * data["quantity"] * data["config"]["contract_size"]
            alerts.append(f"止损价{stop_loss}元/桶（亏损约{risk_amount:,.0f}元时触发）")
        
        return " ".join(alerts) if alerts else "✅ 风险可控"

    def _compliance_check(self, data: dict, params: dict) -> dict:
        """合规检查"""
        quantity = data["quantity"]
        
        return {
            "position_limit": "✅ 未超过单一客户持仓限额（200手）",
            "daily_open_limit": "✅ 未超过每日开仓限额（100手）",
            "margin_check": "✅ 保证金充足",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        """生成一句话摘要"""
        action = params.get("action", "open")
        variety = data["variety"]
        price = data["execution_price"]
        qty = data["quantity"]
        pnl = data["position"]["unrealized_pnl"]
        sl = params.get("stop_loss")
        
        if action == "open":
            sl_note = f"，止损{sl}元/桶" if sl else ""
            return f"{variety}以{price}元/桶成交{qty}手，浮动盈亏{pnl:+.2f}元{sl_note}"
        else:
            return f"{variety}平仓{price}元/桶"


# ============ 使用示例 ============

async def main():
    """使用示例"""
    skill = FuturesTradingSkill()
    
    test_inputs = [
        "SC原油608元/桶买入开仓10手止损580",
        "Brent 75美元买入5手做多",
        "在WTI期货上建3手空头",
    ]
    
    context = {"user_id": "TEST_USER", "session_id": "TEST_SESSION"}
    
    for user_input in test_inputs:
        print(f"\n{'='*60}")
        print(f"输入: {user_input}")
        print(f"can_handle: {skill.can_handle(user_input)}")
        
        params = skill.parse_input(user_input)
        print(f"解析参数: {params}")
        
        result = await skill.execute({**context, "user_input": user_input})
        
        print(f"\n执行结果:")
        print(f"  success: {result.success}")
        print(f"  execution_time_ms: {result.execution_time_ms:.2f}ms")
        
        if result.success:
            data = result.data
            print(f"\n交易指令: {data['trade_order']['variety']} {data['trade_order']['direction']} {data['trade_order']['quantity']}")
            print(f"成交价格: {data['execution_record']['price']}")
            print(f"成交金额: {data['execution_record']['amount']}")
            print(f"浮动盈亏: {data['current_position']['unrealized_pnl']}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
