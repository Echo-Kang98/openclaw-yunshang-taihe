"""
格式化工具
提供货币、百分比、数量等格式化函数
"""


def format_currency(amount: float, currency: str = "CNY", decimals: int = 2) -> str:
    """
    格式化货币金额
    
    Args:
        amount: 金额
        currency: 货币代码 (CNY/USD/EUR)
        decimals: 小数位数
        
    Returns:
        str: 格式化后的字符串，如 "¥1,234.56"
    """
    symbols = {
        "CNY": "¥",
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
    }
    
    symbol = symbols.get(currency, currency + " ")
    formatted_number = f"{abs(amount):,.{decimals}f}"
    
    if amount < 0:
        return f"-{symbol}{formatted_number}"
    return f"{symbol}{formatted_number}"


def format_percentage(value: float, decimals: int = 2, show_sign: bool = False) -> str:
    """
    格式化百分比
    
    Args:
        value: 数值（如0.182表示18.2%）
        decimals: 小数位数
        show_sign: 是否显示正负号
        
    Returns:
        str: 格式化后的字符串，如 "18.20%"
    """
    pct = value * 100 if abs(value) < 10 else value
    sign = "+" if show_sign and pct > 0 else ""
    return f"{sign}{pct:.{decimals}f}%"


def format_large_number(num: float, unit: str = "万") -> str:
    """
    格式化大数字（支持万、亿等单位）
    
    Args:
        num: 数字
        unit: 单位 (万/亿)
        
    Returns:
        str: 格式化后的字符串，如 "1.23万"
    """
    if unit == "万":
        return f"{num / 10000:.2f}万"
    elif unit == "亿":
        return f"{num / 100000000:.2f}亿"
    else:
        return f"{num:,.0f}"
