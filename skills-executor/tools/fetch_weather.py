"""
天气查询工具
预留真实天气API接口（目前使用模拟数据）

真实API预留:
- wttr.in (免费，无需key)
- Open-Meteo (免费，无需key)
- 和风天气 (需要key)
"""

import asyncio
import random
from typing import Optional


async def fetch_weather(city: str = "上海") -> dict:
    """
    获取城市天气
    
    Args:
        city: 城市名称
        
    Returns:
        dict: 天气数据
            - temperature: 温度(℃)
            - condition: 天气状况
            - humidity: 湿度(%)
            - wind_speed: 风速(km/h)
            - source: 数据来源
    """
    # TODO: 接入真实天气API
    # 方案1: wttr.in (免费)
    # import urllib.request
    # url = f"https://wttr.in/{city}?format=j1"
    # response = urllib.request.urlopen(url)
    # data = json.loads(response.read())
    
    # 方案2: Open-Meteo (免费，无需key)
    # url = f"https://api.open-meteo.com/v1/forecast?latitude=31.23&longitude=121.47&current_weather=true"
    
    # 模拟延迟
    await asyncio.sleep(0.1)
    
    # 模拟数据
    conditions = ["晴", "多云", "阴", "小雨", "中雨", "雷阵雨"]
    return {
        "city": city,
        "temperature": round(random.uniform(15, 30), 1),
        "condition": random.choice(conditions),
        "humidity": random.randint(40, 90),
        "wind_speed": round(random.uniform(5, 25), 1),
        "source": "mock",
    }
