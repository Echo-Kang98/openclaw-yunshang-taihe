"""
BaseSkill基类 - 所有Skill的父类
定义Skill的统一接口和行为规范

设计原则:
- 每个Skill独立可测试
- can_handle() 负责快速匹配（同步）
- execute() 负责实际执行（异步，支持真实API调用）
- 所有Skill返回标准 SkillResult 格式
"""

import re
import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Any
from datetime import datetime
from enum import Enum


class OutputFormat(Enum):
    """输出格式枚举"""
    JSON = "json"
    MARKDOWN = "markdown"
    TABLE = "table"
    HTML = "html"


@dataclass
class SkillResult:
    """
    Skill执行结果的标准化封装
    
    Attributes:
        success: 是否成功执行
        skill_name: 执行skill的名称
        output_format: 输出格式
        data: 主数据payload（dict/list/str）
        summary: 一句话摘要（用于飞书通知）
        error: 错误信息（失败时填充）
        execution_time_ms: 执行耗时（毫秒）
        metadata: 附加元数据
    """
    success: bool
    skill_name: str
    output_format: OutputFormat = OutputFormat.JSON
    data: Any = None
    summary: str = ""
    error: Optional[str] = None
    execution_time_ms: float = 0.0
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """转换为字典（JSON序列化友好）"""
        return {
            "success": self.success,
            "skill_name": self.skill_name,
            "output_format": self.output_format.value,
            "data": self.data,
            "summary": self.summary,
            "error": self.error,
            "execution_time_ms": round(self.execution_time_ms, 2),
            "metadata": self.metadata,
            "timestamp": datetime.now().isoformat(),
        }

    def to_markdown(self) -> str:
        """转换为Markdown格式"""
        if not self.success:
            return f"## ❌ {self.skill_name} 执行失败\n\n**错误**: {self.error}"
        
        lines = [f"## {self.skill_name}", f"\n**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ""]
        
        if self.summary:
            lines.append(f"**摘要**: {self.summary}\n")
        
        if isinstance(self.data, dict):
            for key, value in self.data.items():
                if isinstance(value, (dict, list)):
                    lines.append(f"- **{key}**: See data field")
                else:
                    lines.append(f"- **{key}**: {value}")
        elif isinstance(self.data, str):
            lines.append(self.data)
        else:
            lines.append(str(self.data))
        
        return "\n".join(lines)


class BaseSkill(ABC):
    """
    Skill执行器基类
    
    使用方法:
        1. 继承此类
        2. 实现 trigger_keywords 和 optional_keywords
        3. 实现 parse_input() 解析用户输入
        4. 实现 fetch_data() 获取数据（预留API接口）
        5. 实现 generate_output() 生成输出
    
    示例:
        class MySkill(BaseSkill):
            name = "我的技能"
            description = "做什么的"
            trigger_keywords = ["做", "执行"]
            
            def parse_input(self, user_input: str) -> dict:
                # 解析用户输入，返回参数字典
                pass
            
            async def execute(self, context: dict) -> SkillResult:
                start = time.time()
                params = self.parse_input(context.get("user_input", ""))
                data = await self.fetch_data(params)
                output = self.generate_output(data)
                return SkillResult(
                    success=True,
                    skill_name=self.name,
                    data=output,
                    summary=f"执行完成: {output.get('result', 'N/A')}",
                    execution_time_ms=(time.time() - start) * 1000
                )
    """

    # === 类属性（子类必须设置）===
    name: str = "BaseSkill"
    description: str = "基础技能"
    department: str = "通用"
    
    # 触发关键词（必须包含其中之一才能匹配）
    trigger_keywords: list = field(default_factory=list)
    
    # 可选关键词（增强匹配，不必须）
    optional_keywords: list = field(default_factory=list)
    
    # 输入示例（用于调试和文档）
    examples: list = field(default_factory=list)

    def __init__(self):
        self._compiled_patterns = None

    # ========================
    # 公共接口
    # ========================

    def can_handle(self, user_input: str) -> bool:
        """
        判断当前Skill是否能处理该输入
        
        匹配策略:
        1. 必须包含至少一个trigger_keyword
        2. 如果有optional_keywords，则优先匹配
        3. 使用正则表达式实现模糊匹配
        
        Args:
            user_input: 用户输入的原始文本
            
        Returns:
            bool: True=能处理，False=不能处理
        """
        if not user_input or not user_input.strip():
            return False
        
        user_input_lower = user_input.lower()
        
        # 检查触发关键词（至少一个）
        has_trigger = any(
            kw.lower() in user_input_lower 
            for kw in self.trigger_keywords
        )
        if not has_trigger:
            return False
        
        # 如果没有可选关键词，直接通过
        if not self.optional_keywords:
            return True
        
        # 检查可选关键词（至少匹配一个）
        has_optional = any(
            kw.lower() in user_input_lower 
            for kw in self.optional_keywords
        )
        return has_optional

    async def execute(self, context: dict) -> SkillResult:
        """
        执行Skill的核心逻辑
        
        默认实现调用：
        1. parse_input() - 解析输入
        2. fetch_data() - 获取数据（异步）
        3. generate_output() - 生成输出
        
        子类可以重写此方法以实现更复杂的流程。
        
        Args:
            context: 执行上下文，包含:
                - user_input: str 用户输入
                - user_id: str 用户ID
                - session_id: str 会话ID
                - ... 其他上下文数据
                
        Returns:
            SkillResult: 标准化的执行结果
        """
        import time
        start_time = time.time()
        
        try:
            user_input = context.get("user_input", "")
            
            # 1. 解析输入
            params = self._safe_parse_input(user_input)
            
            # 2. 验证参数
            validation_error = self._validate_params(params)
            if validation_error:
                return SkillResult(
                    success=False,
                    skill_name=self.name,
                    error=validation_error,
                    execution_time_ms=(time.time() - start_time) * 1000,
                )
            
            # 3. 获取数据（可被重写为真实API调用）
            data = await self._safe_fetch_data(params, context)
            
            # 4. 生成输出
            output = self._safe_generate_output(data, params)
            
            # 5. 构建结果
            return SkillResult(
                success=True,
                skill_name=self.name,
                data=output,
                summary=output.get("summary", self._generate_summary(data, output, params)),
                execution_time_ms=(time.time() - start_time) * 1000,
                metadata={
                    "department": self.department,
                    "params": params,
                }
            )
            
        except Exception as e:
            return SkillResult(
                success=False,
                skill_name=self.name,
                error=f"执行异常: {str(e)}",
                execution_time_ms=(time.time() - start_time) * 1000,
            )

    def get_output_format(self) -> str:
        """返回默认输出格式"""
        return OutputFormat.JSON.value

    def get_info(self) -> dict:
        """获取Skill的元信息（用于注册和文档）"""
        return {
            "name": self.name,
            "description": self.description,
            "department": self.department,
            "trigger_keywords": self.trigger_keywords,
            "optional_keywords": self.optional_keywords,
            "examples": self.examples,
        }

    # ========================
    # 可重写的方法
    # ========================

    def parse_input(self, user_input: str) -> dict:
        """
        解析用户输入，提取参数
        
        子类应实现此方法，根据trigger_keywords从user_input中提取参数。
        默认实现返回空字典。
        
        Args:
            user_input: 用户输入的原始文本
            
        Returns:
            dict: 解析后的参数字典
        """
        return {}

    def _safe_parse_input(self, user_input: str) -> dict:
        """安全调用parse_input"""
        try:
            return self.parse_input(user_input)
        except Exception as e:
            return {"_parse_error": str(e)}

    def _validate_params(self, params: dict) -> Optional[str]:
        """
        验证参数是否合法
        
        默认不做验证。子类可重写。
        
        Returns:
            str: 错误信息，如果有的话
        """
        return None

    async def fetch_data(self, params: dict, context: dict) -> dict:
        """
        获取执行所需的数据
        
        默认返回模拟数据。子类应重写此方法以调用真实API。
        支持asyncio以实现并发API调用。
        
        Args:
            params: parse_input()解析出的参数字典
            context: 执行上下文
            
        Returns:
            dict: 获取到的数据
        """
        await asyncio.sleep(0.1)  # 模拟API延迟
        return {"_mock": True, "params": params}

    async def _safe_fetch_data(self, params: dict, context: dict) -> dict:
        """安全调用fetch_data"""
        try:
            return await self.fetch_data(params, context)
        except Exception as e:
            raise RuntimeError(f"fetch_data失败: {str(e)}")

    def generate_output(self, data: dict, params: dict) -> dict:
        """
        根据数据生成输出
        
        子类应实现此方法，将fetch_data()返回的数据转换为标准输出格式。
        
        Args:
            data: fetch_data()返回的数据
            params: parse_input()解析出的参数
            
        Returns:
            dict: 标准化的输出数据
        """
        return {"result": "default", "data": data}

    def _safe_generate_output(self, data: dict, params: dict) -> dict:
        """安全调用generate_output"""
        try:
            return self.generate_output(data, params)
        except Exception as e:
            return {"_output_error": str(e), "data": data}

    def _generate_summary(self, data: dict, output: dict, params: dict) -> str:
        """生成一句话摘要（子类应重写）"""
        return f"{self.name} 执行完成"

    # ========================
    # 辅助方法
    # ========================

    def _extract_by_pattern(self, text: str, pattern: str, default: str = None) -> str:
        """使用正则表达式提取文本中的内容"""
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1) if match else default

    def _extract_number(self, text: str, pattern: str, default: float = None) -> float:
        """提取数字"""
        match = re.search(pattern, text)
        if match:
            try:
                return float(match.group(1).replace(",", ""))
            except ValueError:
                pass
        return default
