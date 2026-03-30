"""
消息发送工具
预留飞书/企业微信等消息发送接口

真实API预留:
- 飞书机器人webhook
- 企业微信机器人webhook
- 邮件发送 (SMTP)
"""

import asyncio
from typing import Optional


async def send_feishu_message(webhook_url: str, content: str) -> dict:
    """
    发送飞书机器人消息
    
    Args:
        webhook_url: 飞书机器人webhook地址
        content: 消息内容（Markdown格式）
        
    Returns:
        dict: 发送结果
    """
    # TODO: 接入真实飞书API
    # import requests
    # payload = {
    #     "msg_type": "markdown",
    #     "content": {
    #         "text": content
    #     }
    # }
    # response = requests.post(webhook_url, json=payload)
    # return response.json()
    
    await asyncio.sleep(0.05)
    return {
        "success": True,
        "message_id": f"mock_{asyncio.get_event_loop().time()}",
        "source": "mock",
    }


async def send_wecom_message(webhook_url: str, content: str) -> dict:
    """
    发送企业微信机器人消息
    
    Args:
        webhook_url: 企业微信机器人webhook地址
        content: 消息内容
        
    Returns:
        dict: 发送结果
    """
    # TODO: 接入真实企业微信API
    await asyncio.sleep(0.05)
    return {
        "success": True,
        "errcode": 0,
        "source": "mock",
    }
