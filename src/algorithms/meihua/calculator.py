#!/usr/bin/env python3
"""
梅花易数主计算器
整合各个模块，提供统一的计算接口
"""

import datetime
from typing import Dict, Any

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core import MeiHuaCoreCalculator
from ti_yong import TiYongAnalyzer
from season import SeasonAnalyzer
from formatter import MeiHuaFormatter
from constants import LIUSHI_SIGUA

class MeiHuaCalculator:
    """梅花易数计算器主类"""
    
    @classmethod
    def calculate(cls, num1: int, num2: int, question: str = "", dt: datetime.datetime = None) -> Dict[str, Any]:
        """
        完整的梅花易数计算
        Args:
            num1: 第一个数字（上卦）
            num2: 第二个数字（下卦）
            question: 问题
            dt: 起卦时间，默认为当前时间
        Returns:
            包含完整排盘信息的字典
        """
        if dt is None:
            dt = datetime.datetime.now()
        
        # 1. 基础起卦
        basic_qigua = MeiHuaCoreCalculator.number_qigua(num1, num2)
        
        # 2. 生成本卦、变卦、互卦
        shang_gua_name = basic_qigua["shang_gua"]["name"]
        xia_gua_name = basic_qigua["xia_gua"]["name"]
        dong_yao = basic_qigua["dong_yao"]
        
        ben_gua_yaos = MeiHuaCoreCalculator.generate_ben_gua(shang_gua_name, xia_gua_name)
        ben_gua_name = LIUSHI_SIGUA.get(f"{shang_gua_name}{xia_gua_name}", "未知卦")
        
        bian_gua_yaos = MeiHuaCoreCalculator.generate_bian_gua(ben_gua_yaos, dong_yao)
        bian_gua_info = MeiHuaCoreCalculator.analyze_gua_from_yaos(bian_gua_yaos)
        
        hu_gua_yaos = MeiHuaCoreCalculator.generate_hu_gua(ben_gua_yaos)
        hu_gua_info = MeiHuaCoreCalculator.analyze_gua_from_yaos(hu_gua_yaos)
        
        # 3. 体用分析
        ti_yong = TiYongAnalyzer.determine_ti_yong(dong_yao, shang_gua_name, xia_gua_name)
        
        # 4. 五行生克分析
        wuxing_analysis = TiYongAnalyzer.analyze_wuxing_relations(
            ti_yong["ti_gua"]["name"], ti_yong["yong_gua"]["name"],
            hu_gua_info["shang_gua"], hu_gua_info["xia_gua"],
            bian_gua_info["shang_gua"], bian_gua_info["xia_gua"]
        )
        
        # 5. 时令旺衰分析
        season_analysis = SeasonAnalyzer.analyze_season_strength(
            dt, ti_yong["ti_gua"]["name"], ti_yong["yong_gua"]["name"]
        )
        
        # 6. 组装完整结果
        result = {
            "basic_info": {
                "question": question,
                "qigua_time": dt.strftime("%Y年%m月%d日%H时%M分"),
                "input_numbers": [num1, num2],
                "season": season_analysis["season"],
                "lunar_month": season_analysis["lunar_month"],
                "time_dizhi": season_analysis["time_dizhi"]
            },
            "gua_structure": {
                "ben_gua": {
                    "name": ben_gua_name,
                    "shang_gua": MeiHuaFormatter.format_gua_info(shang_gua_name),
                    "xia_gua": MeiHuaFormatter.format_gua_info(xia_gua_name),
                    "yaos": MeiHuaFormatter.format_yaos_for_llm(ben_gua_yaos),
                    "dong_yao": {
                        "position": dong_yao,
                        "description": f"第{dong_yao}爻动",
                        "yao_nature": "阳爻变阴爻" if ben_gua_yaos[dong_yao-1] == 1 else "阴爻变阳爻"
                    }
                },
                "bian_gua": {
                    "name": bian_gua_info["name"],
                    "shang_gua": MeiHuaFormatter.format_gua_info(bian_gua_info["shang_gua"]) if bian_gua_info["shang_gua"] else None,
                    "xia_gua": MeiHuaFormatter.format_gua_info(bian_gua_info["xia_gua"]) if bian_gua_info["xia_gua"] else None,
                    "yaos": MeiHuaFormatter.format_yaos_for_llm(bian_gua_yaos)
                },
                "hu_gua": {
                    "name": hu_gua_info["name"],
                    "shang_gua": MeiHuaFormatter.format_gua_info(hu_gua_info["shang_gua"]) if hu_gua_info["shang_gua"] else None,
                    "xia_gua": MeiHuaFormatter.format_gua_info(hu_gua_info["xia_gua"]) if hu_gua_info["xia_gua"] else None,
                    "yaos": MeiHuaFormatter.format_yaos_for_llm(hu_gua_yaos)
                }
            },
            "ti_yong_analysis": ti_yong,
            "wuxing_analysis": wuxing_analysis,
            "season_analysis": season_analysis
        }
        
        return result
    
    @classmethod
    def format_for_llm(cls, result: Dict[str, Any]) -> str:
        """格式化为LLM友好的文本"""
        return MeiHuaFormatter.format_for_llm(result)


# 简化的测试函数
def test_meihua_calculator():
    """测试梅花易数计算器"""
    print("=== 模块化梅花易数测试 ===")
    
    result = MeiHuaCalculator.calculate(23, 45, "我的事业发展如何")
    formatted_output = MeiHuaCalculator.format_for_llm(result)
    
    print(formatted_output)
    print("\n" + "="*50)
    print("✅ 模块化梅花易数计算器测试完成！")
    print("✅ 代码结构清晰，只提供信息，不做判断！")


if __name__ == "__main__":
    test_meihua_calculator()