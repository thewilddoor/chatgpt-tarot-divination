#!/usr/bin/env python3
"""
梅花易数核心算法
包含起卦、生成卦象等基础功能
"""

from typing import List, Dict, Any
from constants import *

class MeiHuaCoreCalculator:
    """梅花易数核心计算器"""
    
    
    @classmethod
    def number_group_qigua(cls, numbers: List[int], shichen: int = None) -> Dict[str, Any]:
        """
        数字组起卦法（按新规则）
        Args:
            numbers: 一组数字
            shichen: 时辰（1-12，对应子丑寅卯等）
        Returns:
            基础起卦信息
        """
        if not numbers:
            raise ValueError("数字组不能为空")
        
        # 数字个数
        count = len(numbers)
        
        # 分割数字组
        if count == 1:  # 特殊情况：只有一个数字
            first_half = numbers
            second_half = numbers
        elif count % 2 == 0:  # 偶数个数字：平分为二
            mid = count // 2
            first_half = numbers[:mid]
            second_half = numbers[mid:]
        else:  # 奇数个数字：前部分比后部分少一个数字
            mid = count // 2
            first_half = numbers[:mid]
            second_half = numbers[mid:]
        
        # 计算上卦和下卦
        first_sum = sum(first_half)
        second_sum = sum(second_half)
        
        shang_gua_num = first_sum % 8 if first_sum % 8 != 0 else 8
        xia_gua_num = second_sum % 8 if second_sum % 8 != 0 else 8
        
        # 计算动爻（传统方法：重卦总数除六）
        # 重卦总数 = 上卦数 + 下卦数 + 时辰数
        zhong_gua_total = shang_gua_num + xia_gua_num + (shichen if shichen else 0)
        dong_yao = zhong_gua_total % 6 if zhong_gua_total % 6 != 0 else 6
        
        # 获取卦名
        shang_gua_name = XIANTIAN_BAGUA[shang_gua_num]
        xia_gua_name = XIANTIAN_BAGUA[xia_gua_num]
        
        return {
            "input_numbers": numbers,
            "first_half": first_half,
            "second_half": second_half,
            "first_sum": first_sum,
            "second_sum": second_sum,
            "shichen": shichen,
            "zhong_gua_total": zhong_gua_total,
            "shang_gua": {
                "name": shang_gua_name,
                "number": shang_gua_num,
                "yaos": BAGUA_YAOS[shang_gua_name]
            },
            "xia_gua": {
                "name": xia_gua_name,
                "number": xia_gua_num,
                "yaos": BAGUA_YAOS[xia_gua_name]
            },
            "dong_yao": dong_yao
        }
    
    @classmethod
    def generate_ben_gua(cls, shang_gua: str, xia_gua: str) -> List[int]:
        """生成本卦六爻"""
        return BAGUA_YAOS[xia_gua] + BAGUA_YAOS[shang_gua]
    
    @classmethod
    def generate_bian_gua(cls, ben_gua: List[int], dong_yao: int) -> List[int]:
        """生成变卦（动爻变化）"""
        bian_gua = ben_gua.copy()
        # 动爻变化：阳变阴，阴变阳
        bian_gua[dong_yao - 1] = 1 - bian_gua[dong_yao - 1]
        return bian_gua
    
    @classmethod
    def generate_hu_gua(cls, ben_gua: List[int]) -> List[int]:
        """生成互卦（由2,3,4爻和3,4,5爻组成）"""
        if len(ben_gua) != 6:
            return ben_gua
        
        hu_xia = ben_gua[1:4]  # 2,3,4爻为下卦
        hu_shang = ben_gua[2:5]  # 3,4,5爻为上卦
        return hu_xia + hu_shang
    
    @classmethod
    def analyze_gua_from_yaos(cls, yaos: List[int]) -> Dict[str, Any]:
        """从爻象分析出卦名和属性"""
        if len(yaos) != 6:
            return {"name": "未知卦", "shang_gua": None, "xia_gua": None}
        
        xia_yaos = yaos[0:3]
        shang_yaos = yaos[3:6]
        
        # 查找对应的八卦名
        xia_gua_name = None
        shang_gua_name = None
        
        for gua_name, gua_yaos in BAGUA_YAOS.items():
            if gua_yaos == xia_yaos:
                xia_gua_name = gua_name
            if gua_yaos == shang_yaos:
                shang_gua_name = gua_name
        
        if xia_gua_name and shang_gua_name:
            gua_name = LIUSHI_SIGUA.get(f"{shang_gua_name}{xia_gua_name}", "未知卦")
            return {
                "name": gua_name,
                "shang_gua": shang_gua_name,
                "xia_gua": xia_gua_name
            }
        
        return {"name": "未知卦", "shang_gua": None, "xia_gua": None}