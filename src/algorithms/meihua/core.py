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
    def number_qigua(cls, num1: int, num2: int) -> Dict[str, Any]:
        """
        数字起卦法
        Args:
            num1: 第一个数字（上卦）
            num2: 第二个数字（下卦）
        Returns:
            基础起卦信息
        """
        # 计算上卦、下卦和动爻
        shang_gua_num = num1 % 8 if num1 % 8 != 0 else 8
        xia_gua_num = num2 % 8 if num2 % 8 != 0 else 8
        dong_yao = (num1 + num2) % 6 if (num1 + num2) % 6 != 0 else 6
        
        # 获取卦名
        shang_gua_name = XIANTIAN_BAGUA[shang_gua_num]
        xia_gua_name = XIANTIAN_BAGUA[xia_gua_num]
        
        return {
            "input_numbers": [num1, num2],
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