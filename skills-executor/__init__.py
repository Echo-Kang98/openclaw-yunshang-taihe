"""
云上泰和2.0 - Skills执行框架
Skills Executor Framework for Yunshang Taihe 2.0

提供Skill加载、匹配和执行的核心能力。
"""

__version__ = "0.1.0"
__author__ = "云上泰和工部"

from .base import BaseSkill, SkillResult
from .skill_loader import SkillLoader

__all__ = ["BaseSkill", "SkillResult", "SkillLoader"]
