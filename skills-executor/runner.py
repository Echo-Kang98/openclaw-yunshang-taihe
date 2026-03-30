"""
Skill执行器 - 统一入口
负责加载所有Skill并根据用户输入自动匹配执行

使用示例:
    python runner.py "生成2026年1月财务报表"
    python runner.py "SC原油608元/桶买入开仓10手"
    python runner.py "分析美元/人民币走势"
"""

import asyncio
import sys
import json
from typing import Optional

# 添加父目录到路径
sys.path.insert(0, __file__.rsplit("/", 1)[0])

from base import BaseSkill, SkillResult
from skill_loader import SkillLoader


# 导入所有已实现的Skills
REGISTERED_SKILLS: list[BaseSkill] = []

try:
    import importlib.util
    
    # 动态导入各部门的Skill
    def load_skill_module(path: str, class_name: str):
        spec = importlib.util.spec_from_file_location("skill_module", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, class_name)
    
    executor_dir = __file__.rsplit("/", 1)[0]
    
    # 财务经营部
    fr_path = f"{executor_dir}/skills/财务经营部/financial_report.py"
    FinancialReportSkill = load_skill_module(fr_path, "FinancialReportSkill")
    REGISTERED_SKILLS.append(FinancialReportSkill())
    
    # 期现交易部
    ft_path = f"{executor_dir}/skills/期现交易部/futures_trading.py"
    FuturesTradingSkill = load_skill_module(ft_path, "FuturesTradingSkill")
    REGISTERED_SKILLS.append(FuturesTradingSkill())
    
    # 汇率经营部
    er_path = f"{executor_dir}/skills/汇率经营部/exchange_rate.py"
    ExchangeRateAnalysisSkill = load_skill_module(er_path, "ExchangeRateAnalysisSkill")
    REGISTERED_SKILLS.append(ExchangeRateAnalysisSkill())
    
except Exception as e:
    print(f"⚠️  部分Skill导入失败: {e}")
    import traceback
    traceback.print_exc()


class SkillRunner:
    """
    Skill执行器
    
    功能:
    1. 管理已注册的Skill列表
    2. 根据用户输入自动匹配最合适的Skill
    3. 执行匹配的Skill并返回结果
    4. 支持Skill重排序和优先级
    """

    def __init__(self, skills: list[BaseSkill] = None):
        """
        初始化执行器
        
        Args:
            skills: Skill实例列表，默认为REGISTERED_SKILLS
        """
        self.skills = skills or REGISTERED_SKILLS

    def find_skill(self, user_input: str) -> Optional[BaseSkill]:
        """
        查找最适合处理该输入的Skill
        
        策略:
        1. 遍历所有Skill的can_handle()方法
        2. 返回第一个返回True的Skill
        3. 如果都没匹配，返回None
        
        Args:
            user_input: 用户输入
            
        Returns:
            BaseSkill 或 None
        """
        for skill in self.skills:
            if skill.can_handle(user_input):
                return skill
        return None

    def find_all_matching(self, user_input: str) -> list[tuple[BaseSkill, float]]:
        """
        查找所有匹配的Skill并返回匹配度
        
        Args:
            user_input: 用户输入
            
        Returns:
            list of (Skill, score) 按匹配度降序
        """
        matches = []
        for skill in self.skills:
            if skill.can_handle(user_input):
                # 计算简单匹配度分数
                score = sum(
                    1 for kw in skill.trigger_keywords
                    if kw.lower() in user_input.lower()
                )
                matches.append((skill, score))
        
        return sorted(matches, key=lambda x: x[1], reverse=True)

    async def run(self, user_input: str, context: dict = None) -> SkillResult:
        """
        执行用户输入对应的Skill
        
        Args:
            user_input: 用户输入
            context: 额外上下文
            
        Returns:
            SkillResult: 执行结果
        """
        context = context or {}
        context["user_input"] = user_input
        
        skill = self.find_skill(user_input)
        
        if skill is None:
            return SkillResult(
                success=False,
                skill_name="None",
                error=f"未找到能处理该输入的Skill: {user_input}",
            )
        
        print(f"🎯 匹配到Skill: {skill.name} ({skill.department})")
        
        result = await skill.execute(context)
        return result

    def list_skills(self) -> list[dict]:
        """列出所有已注册的Skill"""
        return [skill.get_info() for skill in self.skills]


async def main():
    """CLI入口"""
    if len(sys.argv) < 2:
        print("=" * 60)
        print("云上泰和2.0 - Skills执行器")
        print("=" * 60)
        print("\n用法:")
        print("  python runner.py <用户输入>")
        print("  python runner.py --list    # 列出所有Skill")
        print("  python runner.py --load    # 加载并解析SKILL.md")
        print("\n示例:")
        print('  python runner.py "生成2026年1月财务报表"')
        print('  python runner.py "SC原油608元/桶买入开仓10手"')
        print('  python runner.py "分析美元/人民币走势"')
        print()
        
        # 显示已注册的Skills
        runner = SkillRunner()
        skills = runner.list_skills()
        print(f"已注册 {len(skills)} 个Skill:\n")
        for skill in skills:
            print(f"  [{skill['department']}] {skill['name']}")
            print(f"    触发: {', '.join(skill['trigger_keywords'][:3])}...")
            print()
        return
    
    user_input = " ".join(sys.argv[1:])
    
    # 特殊命令
    if user_input == "--list":
        runner = SkillRunner()
        skills = runner.list_skills()
        print(json.dumps(skills, ensure_ascii=False, indent=2))
        return
    
    if user_input == "--load":
        loader = SkillLoader()
        definitions = loader.load_all()
        loader.print_all()
        return
    
    # 执行Skill
    runner = SkillRunner()
    
    print(f"\n📥 用户输入: {user_input}")
    print("-" * 60)
    
    # 查找匹配的Skill
    matches = runner.find_all_matching(user_input)
    if matches:
        print(f"🔍 找到 {len(matches)} 个匹配的Skill:")
        for skill, score in matches:
            print(f"  - {skill.name} (score={score})")
        print()
    
    # 执行
    result = await runner.run(user_input)
    
    # 输出结果
    print("=" * 60)
    print("📤 执行结果:")
    print("=" * 60)
    
    if result.success:
        print(f"✅ {result.skill_name}")
        print(f"⏱️  执行耗时: {result.execution_time_ms:.2f}ms")
        print(f"\n📊 输出数据:")
        print(json.dumps(result.data, ensure_ascii=False, indent=2, default=str))
    else:
        print(f"❌ 执行失败: {result.error}")


if __name__ == "__main__":
    asyncio.run(main())
