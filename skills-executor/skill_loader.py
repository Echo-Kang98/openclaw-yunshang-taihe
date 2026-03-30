"""
SKILL.md 解析器
解析云上泰和项目的SKILL.md文件，自动提取Skill元信息

功能:
1. 扫描skills-repo/dept-skills/目录
2. 解析每个SKILL.md文件，提取描述/触发条件/执行步骤/输出格式
3. 将解析结果与已注册的Skill实现类关联
4. 提供Skill查询和匹配能力
"""

import os
import re
import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class SkillDefinition:
    """
    从SKILL.md解析出的Skill定义
    """
    name: str
    file_path: str
    department: str
    description: str
    trigger_conditions: list = field(default_factory=list)
    execution_steps: list = field(default_factory=list)
    output_format: str = ""
    examples: list = field(default_factory=list)
    dependencies: list = field(default_factory=list)
    raw_content: str = ""


class SkillLoader:
    """
    SKILL.md文件加载器和解析器
    
    使用方法:
        loader = SkillLoader("/path/to/skills-repo")
        definitions = loader.load_all()
        
        # 查找特定部门
        finance_skills = loader.load_department("财务经营部")
        
        # 查找特定Skill
        skill = loader.find("财务报表生成")
    """

    def __init__(self, base_path: str = None):
        """
        初始化加载器
        
        Args:
            base_path: skills-repo根目录路径，默认为仓库根目录下的skills-repo
        """
        if base_path is None:
            # 默认使用仓库根目录
            repo_root = Path(__file__).parent.parent
            base_path = repo_root / "skills-repo"
        
        self.base_path = Path(base_path)
        self._definitions: dict[str, SkillDefinition] = {}

    def load_all(self) -> dict[str, SkillDefinition]:
        """
        加载所有SKILL.md文件
        
        Returns:
            dict: {部门名: SkillDefinition}
        """
        self._definitions.clear()
        
        if not self.base_path.exists():
            print(f"⚠️  路径不存在: {self.base_path}")
            return {}
        
        # 遍历所有.md文件
        for md_file in self.base_path.rglob("*.md"):
            # 跳过非SKILL文件（如README）
            if md_file.stem == "README":
                continue
            
            try:
                definition = self._parse_skill_file(md_file)
                if definition:
                    key = f"{definition.department}/{definition.name}"
                    self._definitions[key] = definition
            except Exception as e:
                print(f"⚠️  解析失败 {md_file}: {e}")
        
        return self._definitions

    def load_department(self, dept_name: str) -> dict[str, SkillDefinition]:
        """
        加载特定部门的所有Skill
        
        Args:
            dept_name: 部门名称（目录名）
            
        Returns:
            dict: {Skill名: SkillDefinition}
        """
        dept_path = self.base_path / dept_name
        if not dept_path.exists():
            return {}
        
        result = {}
        for md_file in dept_path.glob("*.md"):
            if md_file.stem == "README":
                continue
            try:
                definition = self._parse_skill_file(md_file)
                if definition:
                    result[definition.name] = definition
            except Exception as e:
                print(f"⚠️  解析失败 {md_file}: {e}")
        
        return result

    def find(self, skill_name: str) -> Optional[SkillDefinition]:
        """
        查找特定Skill
        
        Args:
            skill_name: Skill名称（如"财务报表生成"）
            
        Returns:
            SkillDefinition 或 None
        """
        for key, definition in self._definitions.items():
            if definition.name == skill_name:
                return definition
        return None

    def _parse_skill_file(self, file_path: Path) -> Optional[SkillDefinition]:
        """
        解析单个SKILL.md文件
        
        Args:
            file_path: .md文件路径
            
        Returns:
            SkillDefinition
        """
        content = file_path.read_text(encoding="utf-8")
        
        # 提取部门名称（上级目录）
        department = file_path.parent.name
        
        # 提取Skill名称（文件名，去掉.md）
        name = file_path.stem
        
        # 提取描述（第一个## 描述之后的内容）
        description = self._extract_section(content, "描述", "## ")
        
        # 提取触发条件
        trigger_conditions = self._extract_list(content, "触发条件")
        
        # 提取执行步骤
        execution_steps = self._extract_list(content, "执行步骤")
        
        # 提取输出格式
        output_format = self._extract_code_block(content, "输出格式")
        
        # 提取示例
        examples = self._extract_list(content, "示例")
        
        # 提取依赖
        dependencies = self._extract_dependencies(content)
        
        return SkillDefinition(
            name=name,
            file_path=str(file_path),
            department=department,
            description=description.strip() if description else "",
            trigger_conditions=trigger_conditions,
            execution_steps=execution_steps,
            output_format=output_format.strip() if output_format else "",
            examples=examples,
            dependencies=dependencies,
            raw_content=content,
        )

    def _extract_section(self, content: str, section_name: str, prefix: str = "\n") -> str:
        """提取章节内容"""
        pattern = rf"(?:^|\n)##?\s*{section_name}\s*(?:\n|$)(.*?)(?=(?:\n##)|$)"
        match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        # 备选：直接搜索标题
        pattern2 = rf"{section_name}[：:]\s*(.+?)(?:\n##|\n#|$)"
        match2 = re.search(pattern2, content, re.DOTALL)
        if match2:
            return match2.group(1).strip()
        
        return ""

    def _extract_list(self, content: str, section_name: str) -> list:
        """提取列表项"""
        section = self._extract_section(content, section_name)
        if not section:
            return []
        
        # 提取所有-开头的行
        items = re.findall(r"^[　\s]*[-*]\s*(.+?)$", section, re.MULTILINE)
        return [item.strip() for item in items if item.strip()]

    def _extract_code_block(self, content: str, section_name: str) -> str:
        """提取代码块内容"""
        section = self._extract_section(content, section_name)
        if not section:
            return ""
        
        # 匹配 ``` ... ``` 代码块
        match = re.search(r"```[\w]*\n?(.*?)```", section, re.DOTALL)
        if match:
            return match.group(1).strip()
        
        return section.strip()

    def _extract_dependencies(self, content: str) -> list:
        """提取依赖列表"""
        deps_section = self._extract_section(content, "依赖")
        if not deps_section:
            return []
        
        # 格式：部门_数据源
        deps = re.findall(r"[\u4e00-\u9fa5a-zA-Z]+_[\u4e00-\u9fa5a-zA-Z]+", deps_section)
        return deps

    def print_all(self):
        """打印所有已加载的Skill（用于调试）"""
        print(f"\n📦 共加载 {len(self._definitions)} 个Skill:\n")
        for key, definition in sorted(self._definitions.items()):
            print(f"  [{definition.department}] {definition.name}")
            print(f"    描述: {definition.description[:50]}...")
            print(f"    触发: {', '.join(definition.trigger_conditions[:2])}")
            print()


# ============ CLI入口 ============

if __name__ == "__main__":
    loader = SkillLoader()
    definitions = loader.load_all()
    loader.print_all()
