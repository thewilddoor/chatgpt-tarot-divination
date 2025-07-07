#!/usr/bin/env python3
"""
梅花易数体用分析
确定体卦用卦及其关系
"""

from typing import Dict, Any
from constants import BAGUA_WUXING, WuXing

class TiYongAnalyzer:
    """体用分析器"""
    
    @classmethod
    def determine_ti_yong(cls, dong_yao: int, shang_gua: str, xia_gua: str) -> Dict[str, Any]:
        """
        确定体用关系
        Args:
            dong_yao: 动爻位置
            shang_gua: 上卦名
            xia_gua: 下卦名
        Returns:
            体用关系信息
        """
        if dong_yao in [1, 2, 3]:  # 动爻在下卦
            ti_gua = shang_gua  # 体卦为上卦
            yong_gua = xia_gua  # 用卦为下卦
            dong_yao_position = "下卦"
        else:  # 动爻在上卦
            ti_gua = xia_gua   # 体卦为下卦
            yong_gua = shang_gua  # 用卦为上卦
            dong_yao_position = "上卦"
        
        ti_wuxing = BAGUA_WUXING[ti_gua]
        yong_wuxing = BAGUA_WUXING[yong_gua]
        
        relation = cls._get_wuxing_relation(yong_wuxing, ti_wuxing)
        
        return {
            "ti_gua": {
                "name": ti_gua,
                "wuxing": ti_wuxing.value,
                "role": "体卦代表求测人自己，为主体"
            },
            "yong_gua": {
                "name": yong_gua,
                "wuxing": yong_wuxing.value,
                "role": "用卦代表所测之事，为客体"
            },
            "relation": relation,
            "dong_yao_position": dong_yao_position
        }
    
    @classmethod
    def _get_wuxing_relation(cls, from_element: WuXing, to_element: WuXing) -> str:
        """获取五行关系"""
        if from_element == to_element:
            return "比和"
        
        # 五行相生关系
        sheng_relations = {
            (WuXing.METAL, WuXing.WATER): "金生水",
            (WuXing.WATER, WuXing.WOOD): "水生木",
            (WuXing.WOOD, WuXing.FIRE): "木生火",
            (WuXing.FIRE, WuXing.EARTH): "火生土",
            (WuXing.EARTH, WuXing.METAL): "土生金"
        }
        
        # 五行相克关系
        ke_relations = {
            (WuXing.METAL, WuXing.WOOD): "金克木",
            (WuXing.WOOD, WuXing.EARTH): "木克土",
            (WuXing.EARTH, WuXing.WATER): "土克水",
            (WuXing.WATER, WuXing.FIRE): "水克火",
            (WuXing.FIRE, WuXing.METAL): "火克金"
        }
        
        if (from_element, to_element) in sheng_relations:
            return sheng_relations[(from_element, to_element)]
        elif (from_element, to_element) in ke_relations:
            return ke_relations[(from_element, to_element)]
        elif (to_element, from_element) in sheng_relations:
            return f"{to_element.value}被{from_element.value}生"
        elif (to_element, from_element) in ke_relations:
            return f"{to_element.value}被{from_element.value}克"
        
        return "无明显关系"
    
    @classmethod
    def analyze_wuxing_relations(cls, ti_gua: str, yong_gua: str, hu_shang: str, hu_xia: str, 
                                bian_shang: str, bian_xia: str) -> Dict[str, Any]:
        """分析五行生克关系"""
        ti_wuxing = BAGUA_WUXING[ti_gua]
        yong_wuxing = BAGUA_WUXING[yong_gua]
        
        # 分析各卦对体卦的影响
        relations = {
            "ti_yong_relation": cls._get_wuxing_relation(yong_wuxing, ti_wuxing),
            "hu_shang_to_ti": cls._get_wuxing_relation(BAGUA_WUXING[hu_shang], ti_wuxing),
            "hu_xia_to_ti": cls._get_wuxing_relation(BAGUA_WUXING[hu_xia], ti_wuxing),
            "bian_shang_to_ti": cls._get_wuxing_relation(BAGUA_WUXING[bian_shang], ti_wuxing),
            "bian_xia_to_ti": cls._get_wuxing_relation(BAGUA_WUXING[bian_xia], ti_wuxing)
        }
        
        return {
            "ti_wuxing": ti_wuxing.value,
            "yong_wuxing": yong_wuxing.value,
            "relations": relations
        }