"""
单据与文件管理 Skill - 交易执行部
管理贸易单据：提单B/L、发票INV、装箱单PL、原产地证CO、商检证书CIQ
"""

import re
import asyncio
import random
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, str(__file__).rsplit("/skills/", 1)[0])
from base import BaseSkill, SkillResult, OutputFormat


class DocumentManagementSkill(BaseSkill):
    """
    单据与文件管理
    
    触发条件:
    - 用户说"单据"、"提单"、"B/L"
    - 用户说"发票"、"INV"、"装箱单"
    - 用户说"产地证"、"商检"
    - 用户说"单证一致"、"审核"
    """

    name = "单据与文件管理"
    description = "管理提单B/L、发票INV、装箱单PL、原产地证CO、商检证书CIQ，确保单证一致"
    department = "交易执行部"
    
    trigger_keywords = [
        "单据", "提单", "B/L", "发票", "INV",
        "装箱单", "PL", "产地证", "CO", "商检", "CIQ",
        "单证一致", "审核单据", "单据管理",
    ]
    
    optional_keywords = [
        "制作", "审核", "归档", "签发", "跟踪",
    ]
    
    examples = [
        "审核这份提单",
        "制作产地证",
        "查看单据状态",
    ]

    def parse_input(self, user_input: str) -> dict:
        params = {
            "doc_type": None,
            "action": None,
        }
        
        doc_patterns = [
            (r"提单|B/L", "BL"),
            (r"发票|INV", "INV"),
            (r"装箱单|PL", "PL"),
            (r"产地证|CO", "CO"),
            (r"商检|CIQ", "CIQ"),
        ]
        for pattern, dtype in doc_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                params["doc_type"] = dtype
                break
        
        if re.search(r"制作|新建|起草", user_input):
            params["action"] = "create"
        elif re.search(r"审核|核对|检查", user_input):
            params["action"] = "review"
        elif re.search(r"归档|存档", user_input):
            params["action"] = "archive"
        elif re.search(r"状态|查看|列表", user_input):
            params["action"] = "list"
        
        return params

    async def fetch_data(self, params: dict, context: dict) -> dict:
        await asyncio.sleep(0.2)
        return {
            "documents": [
                {"type": "提单 B/L", "no": "BL-20260315-001", "contract": "CTR-20260301", "status": "已签发", "date": "2026-03-15", "issue_to": "客户A"},
                {"type": "商业发票 INV", "no": "INV-20260320-002", "contract": "CTR-20260301", "status": "已开具", "date": "2026-03-20", "amount": 580000},
                {"type": "装箱单 PL", "no": "PL-20260315-001", "contract": "CTR-20260301", "status": "已归档", "date": "2026-03-15"},
                {"type": "原产地证 CO", "no": "CO-20260318-001", "contract": "CTR-20260302", "status": "审核中", "date": "2026-03-18"},
                {"type": "商检证书 CIQ", "no": "CIQ-20260319-001", "contract": "CTR-20260302", "status": "待办理", "date": "2026-03-19"},
            ]
        }

    def generate_output(self, data: dict, params: dict) -> dict:
        docs = data["documents"]
        pending = [d for d in docs if d["status"] in ["审核中", "待办理"]]
        return {
            "type": "单据管理概览",
            "total": len(docs),
            "issued": sum(1 for d in docs if "已" in d["status"]),
            "pending": len(pending),
            "document_list": docs,
            "pending_list": pending,
            "summary": f"共{len(docs)}份单据，已签发{sum(1 for d in docs if '已' in d['status'])}份，待处理{len(pending)}份",
        }

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        return output.get("summary", "单据数据已生成")
