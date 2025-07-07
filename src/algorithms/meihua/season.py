#!/usr/bin/env python3
"""
梅花易数时令旺衰分析
分析八卦在不同时节的旺相休囚死状态
"""

import datetime
from typing import Dict, Any
from constants import BAGUA_WUXING, SEASON_STRENGTH, SeasonState

class SeasonAnalyzer:
    """时令旺衰分析器"""
    
    @classmethod
    def analyze_season_strength(cls, dt: datetime.datetime, ti_gua: str, yong_gua: str) -> Dict[str, Any]:
        """
        分析时令旺衰
        Args:
            dt: 时间
            ti_gua: 体卦名
            yong_gua: 用卦名
        Returns:
            时令旺衰分析结果
        """
        season = cls._get_season(dt.month)
        month = dt.month
        
        # 获取当前季节的五行强度表
        current_strength = SEASON_STRENGTH[season].copy()
        
        # 土在四季月（辰、未、戌、丑月）旺
        if month in [3, 6, 9, 12]:
            current_strength[BAGUA_WUXING["坤"]] = SeasonState.WANG
        
        ti_wuxing = BAGUA_WUXING[ti_gua]
        yong_wuxing = BAGUA_WUXING[yong_gua]
        
        return {
            "season": season,
            "month": month,
            "lunar_month": cls._get_lunar_month(month),
            "time_dizhi": cls._get_time_dizhi(dt.hour),
            "ti_gua_strength": {
                "gua_name": ti_gua,
                "wuxing": ti_wuxing.value,
                "state": current_strength[ti_wuxing].value,
                "description": cls._get_strength_description(current_strength[ti_wuxing])
            },
            "yong_gua_strength": {
                "gua_name": yong_gua,
                "wuxing": yong_wuxing.value,
                "state": current_strength[yong_wuxing].value,
                "description": cls._get_strength_description(current_strength[yong_wuxing])
            }
        }
    
    @classmethod
    def _get_season(cls, month: int) -> str:
        """获取季节"""
        if month in [3, 4, 5]:
            return "春"
        elif month in [6, 7, 8]:
            return "夏"
        elif month in [9, 10, 11]:
            return "秋"
        else:
            return "冬"
    
    @classmethod
    def _get_lunar_month(cls, month: int) -> str:
        """获取农历月份（简化）"""
        lunar_months = ["正月", "二月", "三月", "四月", "五月", "六月",
                       "七月", "八月", "九月", "十月", "十一月", "十二月"]
        return lunar_months[month - 1]
    
    @classmethod
    def _get_time_dizhi(cls, hour: int) -> str:
        """获取时辰地支"""
        hour_ranges = [
            (23, 1, "子"), (1, 3, "丑"), (3, 5, "寅"), (5, 7, "卯"),
            (7, 9, "辰"), (9, 11, "巳"), (11, 13, "午"), (13, 15, "未"),
            (15, 17, "申"), (17, 19, "酉"), (19, 21, "戌"), (21, 23, "亥")
        ]
        
        for start, end, dizhi in hour_ranges:
            if start <= hour < end or (start == 23 and hour >= 23):
                return dizhi
        return "子"
    
    @classmethod
    def _get_strength_description(cls, state: SeasonState) -> str:
        """获取旺衰状态描述"""
        descriptions = {
            SeasonState.WANG: "当令而旺，力量最强",
            SeasonState.XIANG: "得令相助，力量较强",
            SeasonState.XIU: "休息状态，力量平常",
            SeasonState.QIU: "受制约束，力量衰弱",
            SeasonState.SI: "克制严重，力量最弱"
        }
        return descriptions[state]