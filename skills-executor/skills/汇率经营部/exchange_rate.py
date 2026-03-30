"""
汇率走势分析 Skill
分析人民币/美元、欧元等主要货币汇率走势，为外汇决策提供支持

输入: 货币对（USD/CNY）
输出: 趋势+目标位+风险
"""

import re
import asyncio
import random
from datetime import datetime, timedelta
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


# 货币对配置
CURRENCY_PAIR_CONFIGS = {
    "USD/CNY": {
        "base": "USD",
        "quote": "CNY",
        "name": "美元/人民币",
        "tick_size": 0.0001,
        "typical_spread": 0.0005,
    },
    "EUR/CNY": {
        "base": "EUR",
        "quote": "CNY",
        "name": "欧元/人民币",
        "tick_size": 0.0001,
        "typical_spread": 0.0008,
    },
    "EUR/USD": {
        "base": "EUR",
        "quote": "USD",
        "name": "欧元/美元",
        "tick_size": 0.0001,
        "typical_spread": 0.0003,
    },
}


class ExchangeRateAnalysisSkill(BaseSkill):
    """
    汇率走势分析Skill
    
    触发条件:
    - 用户说"美元/人民币接下来怎么走"
    - 月度汇率分析会议前
    - 重大宏观事件（美联储加息/中国GDP发布）后
    
    分析维度:
    - 基本面：美元指数、中美利差、贸易顺差、外汇储备
    - 技术面：支撑位/阻力位、趋势判断
    - 综合研判：短期（1-2周）和中期（1-3月）
    """

    name = "汇率走势分析"
    description = "分析人民币/美元、欧元等主要货币汇率走势，为外汇决策提供支持"
    department = "汇率经营部"
    
    trigger_keywords = [
        "汇率", "走势", "美元", "人民币", "欧元", "日元", "英镑",
        "USD", "CNY", "EUR", "JPY", "GBP",
        "外汇", "结汇", "购汇", "贬值", "升值",
        "美联储", "加息", "降息",
    ]
    
    optional_keywords = [
        "分析", "走势", "怎么走", "预期", "预测", "研判",
        "接下来", "未来", "短期", "中期",
    ]
    
    examples = [
        "分析美元/人民币未来一个月走势",
        "USD/CNY接下来怎么走",
        "人民币会继续贬值吗",
        "欧元/美元走势分析",
    ]

    def parse_input(self, user_input: str) -> dict:
        """
        解析汇率分析请求
        
        支持格式:
        - "分析美元/人民币走势" -> pair="USD/CNY", horizon="both"
        - "USD/CNY接下来怎么走" -> pair="USD/CNY", horizon="short"
        - "人民币会贬值吗" -> pair="USD/CNY", direction="CNY_weaken"
        """
        params = {
            "pair": None,
            "horizon": "both",  # short / medium / both
            "focus": None,  # CNY / USD / trend
        }
        
        # 识别货币对
        pair_patterns = [
            (r"USD/CNY|美元/人民币|美元人民币", "USD/CNY"),
            (r"EUR/CNY|欧元/人民币|欧元人民币", "EUR/CNY"),
            (r"EUR/USD|欧元/美元|欧元美元", "EUR/USD"),
            (r"JPY/CNY|日元/人民币|日元人民币", "JPY/CNY"),
            (r"GBP/CNY|英镑/人民币|英镑人民币", "GBP/CNY"),
        ]
        for pattern, pair in pair_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                params["pair"] = pair
                break
        
        # 如果没有指定货币对，根据上下文推断
        if params["pair"] is None:
            if "美元" in user_input or "USD" in user_input.upper():
                params["pair"] = "USD/CNY"
            elif "欧元" in user_input or "EUR" in user_input.upper():
                params["pair"] = "EUR/USD"
            else:
                params["pair"] = "USD/CNY"  # 默认
        
        # 识别分析周期
        if any(kw in user_input for kw in ["短期", "1-2周", "未来一周", "这周"]):
            params["horizon"] = "short"
        elif any(kw in user_input for kw in ["中期", "1-3月", "未来一月", "本月", "长期"]):
            params["horizon"] = "medium"
        
        # 识别关注点
        if any(kw in user_input for kw in ["贬值", "走弱", "压力"]):
            params["focus"] = "CNY_weaken"
        elif any(kw in user_input for kw in ["升值", "走强", "支撑"]):
            params["focus"] = "CNY_strongen"
        
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        """
        获取汇率分析所需数据
        
        TODO: 接入真实数据源
        - Wind/Bloomberg/路透
        - 中国人民银行汇率数据
        - 外部宏观数据
        
        目前使用模拟数据
        """
        await asyncio.sleep(0.2)  # 模拟API延迟
        
        pair = params.get("pair", "USD/CNY")
        config = CURRENCY_PAIR_CONFIGS.get(pair, CURRENCY_PAIR_CONFIGS["USD/CNY"])
        
        # 模拟即期汇率
        if pair == "USD/CNY":
            spot_rate = random.uniform(7.20, 7.35)
            forward_rate = spot_rate + random.uniform(-0.03, 0.02)  # 一年远期
        elif pair == "EUR/USD":
            spot_rate = random.uniform(1.05, 1.12)
            forward_rate = spot_rate + random.uniform(-0.02, 0.02)
        else:
            spot_rate = random.uniform(7.5, 8.5)
            forward_rate = spot_rate + random.uniform(-0.05, 0.05)
        
        # 模拟驱动因素
        dxy = random.uniform(102, 108)  # 美元指数
        us10y = random.uniform(4.2, 4.8)  # 美国10年期国债收益率
        cn10y = random.uniform(2.5, 3.0)  # 中国10年期国债收益率
        interest_diff = us10y - cn10y  # 中美利差
        
        # 模拟技术面
        support1 = round(spot_rate - 0.02, 4)
        support2 = round(spot_rate - 0.04, 4)
        resistance1 = round(spot_rate + 0.02, 4)
        resistance2 = round(spot_rate + 0.04, 4)
        
        # 模拟趋势判断
        trends = ["震荡偏强", "震荡偏弱", "区间震荡", "趋势上涨", "趋势下跌"]
        trend = random.choice(trends)
        
        # 隐含贬值预期
        implied_depreciation = ((forward_rate - spot_rate) / spot_rate) * 100
        
        return {
            "pair": pair,
            "config": config,
            "timestamp": datetime.now().isoformat(),
            
            # 汇率现状
            "spot_rate": round(spot_rate, 4),
            "forward_rate": round(forward_rate, 4),
            "implied_depreciation": round(implied_depreciation, 2),
            
            # 驱动因素
            "drivers": {
                "dxy": {
                    "value": round(dxy, 1),
                    "trend": "反弹中" if dxy > 104 else "回落中",
                    "impact": "USD↑" if dxy > 104 else "USD↓",
                    "weight": "30%",
                },
                "interest_diff": {
                    "value": round(interest_diff, 1),
                    "unit": "BP",
                    "trend": "利差扩大" if interest_diff > 1.5 else "利差收窄",
                    "impact": "CNY↓" if interest_diff > 0 else "CNY↑",
                    "weight": "35%",
                },
                "trade_balance": {
                    "value": random.randint(400, 700),
                    "unit": "亿美元",
                    "trend": "顺差扩大" if random.random() > 0.5 else "顺差收窄",
                    "impact": "CNY↑" if random.random() > 0.5 else "CNY↓",
                    "weight": "20%",
                },
                "capital_flow": {
                    "value": random.randint(-100, 200),
                    "unit": "亿美元",
                    "trend": "净流入" if random.random() > 0.5 else "净流出",
                    "impact": "CNY↑" if random.random() > 0.5 else "CNY↓",
                    "weight": "15%",
                },
            },
            
            # 技术面
            "technical": {
                "support": [support1, support2],
                "resistance": [resistance1, resistance2],
                "trend": trend,
                "ma_20": round(spot_rate * random.uniform(0.995, 1.005), 4),
                "ma_60": round(spot_rate * random.uniform(0.99, 1.01), 4),
            },
            
            # 综合研判
            "forecast": self._generate_forecast(spot_rate, trend, support1, resistance1),
        }

    def _generate_forecast(self, spot_rate: float, trend: str, support: float, resistance: float) -> dict:
        """生成汇率预测"""
        # 短期预测（1-2周）
        if "强" in trend or "上涨" in trend:
            short_target = round(resistance, 4)
            short_prob = random.uniform(55, 70)
        elif "弱" in trend or "下跌" in trend:
            short_target = round(support, 4)
            short_prob = random.uniform(55, 70)
        else:
            short_target = round((support + resistance) / 2, 4)
            short_prob = random.uniform(45, 55)
        
        # 中期预测（1-3月）
        medium_move = random.uniform(0, 0.08) * (1 if random.random() > 0.5 else -1)
        medium_target = round(spot_rate + medium_move, 4)
        medium_prob = random.uniform(50, 60)
        
        return {
            "short_term": {
                "range": f"{round(min(spot_rate, short_target), 4)}-{round(max(spot_rate, short_target), 4)}",
                "direction": "倾向测试" + (f"{resistance}" if short_target > spot_rate else f"{support}"),
                "target": short_target,
                "probability": f"{short_prob:.0f}%",
            },
            "medium_term": {
                "direction": "破{resistance}概率" if medium_target > spot_rate else "下探{support}概率",
                "target": medium_target,
                "probability": f"{medium_prob:.0f}%",
            },
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        """
        生成汇率分析报告
        """
        pair = data["pair"]
        config = data["config"]
        spot = data["spot_rate"]
        forward = data["forward_rate"]
        
        # 贸易建议
        trade_advice = self._generate_trade_advice(data, params)
        
        return {
            "report_type": "汇率走势分析报告",
            "analysis_date": datetime.now().strftime("%Y-%m-%d"),
            "analysis_horizon": params.get("horizon", "both"),
            
            # 汇率现状
            "rate现状": {
                "pair_name": config["name"],
                "spot": spot,
                "forward_1y": forward,
                "implied_depreciation": f"{data['implied_depreciation']}%（年化）",
            },
            
            # 驱动因素
            "drivers": {
                "美元指数(DXY)": data["drivers"]["dxy"],
                "中美利差": data["drivers"]["interest_diff"],
                "贸易顺差": data["drivers"]["trade_balance"],
                "外资流入": data["drivers"]["capital_flow"],
            },
            
            # 技术面
            "technical": {
                "支撑位": " / ".join([str(s) for s in data["technical"]["support"]]),
                "阻力位": " / ".join([str(r) for r in data["technical"]["resistance"]]),
                "趋势判断": data["technical"]["trend"],
                "MA20": data["technical"]["ma_20"],
                "MA60": data["technical"]["ma_60"],
            },
            
            # 综合研判
            "forecast": data["forecast"],
            
            # 贸易建议
            "trade_advice": trade_advice,
        }

    def _generate_trade_advice(self, data: dict, params: dict) -> dict:
        """生成贸易建议"""
        spot = data["spot_rate"]
        resistance = data["technical"]["resistance"][0]
        support = data["technical"]["support"][0]
        
        advice = {}
        
        # 结汇建议
        if spot >= resistance:
            advice["结汇"] = f"✅ 当前{spot}已达阻力位，建议加大结汇比例至80%"
        elif spot >= (resistance + support) / 2:
            advice["结汇"] = f"⚠️ 当前{spot}处于中间位置，可分批结汇50%"
        else:
            advice["结汇"] = f"⏸️ 暂缓结汇，等待回调至{resistance}以上"
        
        # 购汇建议
        if spot <= support:
            advice["购汇"] = f"✅ 当前{spot}已至支撑位，可适度购汇"
        elif spot <= (resistance + support) / 2:
            advice["购汇"] = f"⏸️ 当前{spot}可少量购汇对冲风险"
        else:
            advice["购汇"] = f"⚠️ 暂缓购汇，等待回调至{support}以下"
        
        # 对冲建议
        advice["对冲"] = "建议持有50%的美元敞口进行远期锁定"
        
        return advice

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        """生成一句话摘要"""
        pair = data["pair"]
        spot = data["spot_rate"]
        short_range = data["forecast"]["short_term"]["range"]
        medium_direction = data["forecast"]["medium_term"]["direction"]
        medium_target = data["forecast"]["medium_term"]["target"]
        medium_prob = data["forecast"]["medium_term"]["probability"]
        
        return (
            f"{pair}即期{spot}，"
            f"短期{short_range}震荡，"
            f"{medium_direction}至{medium_target}（概率{medium_prob}）"
        )


# ============ 使用示例 ============

async def main():
    """使用示例"""
    skill = ExchangeRateAnalysisSkill()
    
    test_inputs = [
        "分析美元/人民币未来一个月走势",
        "USD/CNY接下来怎么走",
        "人民币会继续贬值吗",
        "EUR/USD走势分析",
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
            print(f"\n货币对: {data['rate现状']['pair_name']}")
            print(f"即期汇率: {data['rate现状']['spot']}")
            print(f"隐含贬值预期: {data['rate现状']['implied_depreciation']}")
            print(f"\n短期预测: {data['forecast']['short_term']['range']}")
            print(f"中期预测: {data['forecast']['medium_term']['direction']}")
            print(f"\n结汇建议: {data['trade_advice']['结汇']}")
            print(f"购汇建议: {data['trade_advice']['购汇']}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
