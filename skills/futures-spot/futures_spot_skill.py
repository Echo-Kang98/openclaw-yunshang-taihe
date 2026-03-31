"""
FuturesSpot Skill - 期现交易部综合技能
管理期货交易执行、套利策略分析、期现对冲策略、期货账户风险管理
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class FuturesSpotSkill(BaseSkill):
    """
    期现交易部综合技能
    
    触发条件:
    - 用户说"期货"、"合约"、"开仓"、"平仓"、"持仓"
    - 用户说"套利"、"对冲"、"保证金"
    - 用户说"SC"、"Brent"、"WTI"、"Dubai"
    """

    name = "期现交易部综合技能"
    description = "管理期货交易执行、套利策略、期现对冲、账户风险管理"
    department = "期现交易部"
    
    trigger_keywords = [
        "期货", "合约", "开仓", "平仓", "持仓",
        "套利", "对冲", "保证金",
        "SC", "Brent", "WTI", "Dubai",
        "期现", "期货账户", "强平", "追保",
    ]
    
    optional_keywords = [
        "分析", "策略", "执行", "监控", "建议",
    ]
    
    examples = [
        "分析SC-Brent跨品种套利机会",
        "生成本周期货账户风险报告",
        "建议一个期现对冲策略",
    ]

    def parse_input(self, user_input: str) -> dict:
        params = {
            "sub_skill": None,  # trading/arbitrage/hedging/risk
            "variety": None,
            "direction": None,
            "action": None,
        }
        
        if re.search(r"套利", user_input):
            params["sub_skill"] = "arbitrage"
        elif re.search(r"对冲|套保", user_input):
            params["sub_skill"] = "hedging"
        elif re.search(r"风险|保证金|强平|追保", user_input):
            params["sub_skill"] = "risk"
        else:
            params["sub_skill"] = "trading"
        
        variety_patterns = [
            (r"SC原油?|SC0?", "SC"),
            (r"Brent|BRENT", "BRENT"),
            (r"WTI", "WTI"),
            (r"Dubai|DUBAI", "DUBAI"),
        ]
        for pattern, variety in variety_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                params["variety"] = variety
                break
        
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        sub_skill = params.get("sub_skill")
        
        if sub_skill == "arbitrage":
            return self._mock_arbitrage_data(params)
        elif sub_skill == "hedging":
            return self._mock_hedging_data(params)
        elif sub_skill == "risk":
            return self._mock_risk_data(params)
        return self._mock_trading_data(params)

    def _mock_arbitrage_data(self, params: dict) -> dict:
        sc_price = random.uniform(580, 650)
        brent_price = random.uniform(70, 85) * 7.2
        spread = sc_price - brent_price
        hist_spread = 25.0
        z_score = (spread - hist_spread) / 15.0
        
        return {
            "arbitrage_type": "跨品种套利",
            "pair": "SC-Brent",
            "sc_price": round(sc_price, 1),
            "brent_price_cny": round(brent_price, 1),
            "current_spread": round(spread, 1),
            "historical_spread": hist_spread,
            "z_score": round(z_score, 2),
            "signal": "机会不足" if abs(z_score) < 1.5 else ("买入SC/卖出Brent" if z_score < -1.5 else "观望"),
            "confidence": 0.75 if abs(z_score) > 2 else 0.4,
        }

    def _mock_hedging_data(self, params: dict) -> dict:
        variety = params.get("variety", "SC")
        spot_price = random.uniform(580, 650) if variety == "SC" else random.uniform(70, 85) * 7.2
        futures_price = spot_price * 1.02
        
        return {
            "variety": variety,
            "spot_price": round(spot_price, 1),
            "futures_price": round(futures_price, 1),
            "basis": round(spot_price - futures_price, 1),
            "hedge_ratio": 0.9,
            "recommended_contracts": 10,
            "estimated_cost": round(futures_price * 10 * 1000 * 0.00012, 2),
            "effectiveness": "85%",
        }

    def _mock_risk_data(self, params: dict) -> dict:
        return {
            "account_balance": 5000.0,
            "margin_used": 2800.0,
            "available": 2200.0,
            "risk_level": round(2800 / 5000 * 100, 1),
            "positions": [
                {"variety": "SC", "direction": "long", "qty": 10, "open_price": 620.0, "current_price": 615.0},
                {"variety": "Brent", "direction": "short", "qty": 5, "open_price": 520.0, "current_price": 525.0},
            ],
            "margin_calls": [],
            "force_liquidations": [],
        }

    def _mock_trading_data(self, params: dict) -> dict:
        return {
            "variety": params.get("variety", "SC"),
            "current_price": random.uniform(580, 650),
            "change": random.uniform(-2, 2),
            "volume": random.randint(50000, 200000),
            "open_interest": random.randint(100000, 500000),
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        sub_skill = params.get("sub_skill")
        
        if sub_skill == "arbitrage":
            return self._generate_arbitrage_output(data, params)
        elif sub_skill == "hedging":
            return self._generate_hedging_output(data, params)
        elif sub_skill == "risk":
            return self._generate_risk_output(data, params)
        return self._generate_trading_output(data, params)

    def _generate_arbitrage_output(self, data: dict, params: dict) -> dict:
        return {
            "type": "套利策略分析",
            "pair": data["pair"],
            "current_spread": f"¥{data['current_spread']}元/桶",
            "historical_spread": f"¥{data['historical_spread']}元/桶",
            "z_score": data["z_score"],
            "signal": data["signal"],
            "confidence": f"{data['confidence']*100:.0f}%",
            "summary": f"{data['pair']}价差Z-score={data['z_score']}，信号：{data['signal']}",
        }

    def _generate_hedging_output(self, data: dict, params: dict) -> dict:
        return {
            "type": "期现对冲策略",
            "variety": data["variety"],
            "spot_price": f"¥{data['spot_price']}元/桶",
            "futures_price": f"¥{data['futures_price']}元/桶",
            "hedge_ratio": data["hedge_ratio"],
            "recommended_contracts": f"{data['recommended_contracts']}手",
            "estimated_cost": f"¥{data['estimated_cost']}元",
            "effectiveness": data["effectiveness"],
            "summary": f"建议对冲比例{data['hedge_ratio']}，需{data['recommended_contracts']}手期货合约",
        }

    def _generate_risk_output(self, data: dict, params: dict) -> dict:
        risk = data["risk_level"]
        risk_status = "🟢正常" if risk < 60 else "🟡关注" if risk < 80 else "🟠预警" if risk < 100 else "🔴危险"
        return {
            "type": "期货账户风险报告",
            "account_balance": f"¥{data['account_balance']:,.1f}万",
            "margin_used": f"¥{data['margin_used']:,.1f}万",
            "available": f"¥{data['available']:,.1f}万",
            "risk_level": f"{risk}%",
            "risk_status": risk_status,
            "margin_calls": data["margin_calls"],
            "summary": f"账户风险度{risk}%，{risk_status}，保证金余额¥{data['available']:,.1f}万",
        }

    def _generate_trading_output(self, data: dict, params: dict) -> dict:
        return {
            "type": "期货行情",
            "variety": data["variety"],
            "current_price": f"¥{data['current_price']:.1f}",
            "change": f"{data['change']:+.1f}%",
            "volume": f"{data['volume']:,}手",
            "open_interest": f"{data['open_interest']:,}手",
            "summary": f"{data['variety']}现价¥{data['current_price']:.1f}，涨跌{data['change']:+.1f}%",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "期现交易数据已生成")
