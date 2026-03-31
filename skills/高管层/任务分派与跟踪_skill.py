"""
任务分派与跟踪 Skill - 高管层
高管指令分派、进度跟踪、催办督办
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class TaskAssignmentSkill(BaseSkill):
    name = "任务分派与跟踪"
    description = "高管指令分派、进度跟踪、催办督办"
    department = "高管层"
    
    trigger_keywords = ["任务分派", "指令分派", "任务跟踪", "催办", "督办", "待办"]
    optional_keywords = ["查看", "跟踪", "分派"]
    examples = ["查看待办任务", "催办某事项"]

    def parse_input(self, user_input: str) -> dict:
        return {}

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        return {
            "tasks": [
                {"id": "TASK-001", "title": "完成季度报告", "dept": "经营管理部", "status": "进行中", "progress": 60},
                {"id": "TASK-002", "title": "供应商评审", "dept": "国际交易部", "status": "待开始", "progress": 0},
            ]
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        tasks = data["tasks"]
        return {
            "type": "任务跟踪概览",
            "total": len(tasks),
            "in_progress": sum(1 for t in tasks if t["status"] == "进行中"),
            "pending": sum(1 for t in tasks if t["status"] in ["待开始", "待处理"]),
            "task_list": tasks,
            "summary": f"共{len(tasks)}个任务，{sum(1 for t in tasks if t['status']=='进行中')}进行中，{sum(1 for t in tasks if t['status'] in ['待开始','待处理'])}待处理",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "任务数据已生成")
