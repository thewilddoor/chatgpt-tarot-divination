#!/usr/bin/env python3
"""
梅花易数输出格式化
为LLM优化的结构化输出
"""

from typing import List, Dict, Any
from constants import BAGUA_ATTRIBUTES, BAGUA_DIRECTION, BAGUA_WUXING

class MeiHuaFormatter:
    """梅花易数格式化器"""
    
    @classmethod
    def format_yaos_for_llm(cls, yaos: List[int]) -> Dict[str, Any]:
        """为LLM优化的爻象格式"""
        yao_names = ["初", "二", "三", "四", "五", "上"]
        yao_positions = ["下卦初爻", "下卦二爻", "下卦三爻", "上卦四爻", "上卦五爻", "上卦六爻"]
        
        formatted_yaos = []
        for i, yao in enumerate(yaos):
            formatted_yaos.append({
                "position": yao_names[i],
                "full_position": yao_positions[i],
                "value": "阳爻" if yao == 1 else "阴爻",
                "symbol": "━━━" if yao == 1 else "━ ━",
                "number": yao
            })
        
        return {
            "structure": formatted_yaos,
            "description": f"从下到上：{' '.join([yao['value'] for yao in formatted_yaos])}",
            "binary_format": "".join(["1" if yao == 1 else "0" for yao in yaos])
        }
    
    @classmethod
    def format_gua_info(cls, gua_name: str) -> Dict[str, Any]:
        """格式化卦的详细信息"""
        return {
            "name": gua_name,
            "wuxing": BAGUA_WUXING[gua_name].value,
            "direction": BAGUA_DIRECTION[gua_name],
            "attributes": BAGUA_ATTRIBUTES[gua_name]
        }
    
    @classmethod
    def format_for_llm(cls, result: Dict[str, Any]) -> str:
        """为专业梅花易数解卦AI优化的格式"""
        lines = []
        
        # 基本信息
        basic = result["basic_info"]
        lines.append("=== 梅花易数完整排盘信息 ===")
        lines.append(f"起卦时间：{basic['qigua_time']}")
        lines.append(f"起卦数字：{basic['input_numbers'][0]} 和 {basic['input_numbers'][1]}")
        lines.append(f"时令季节：{basic['season']}季 {basic['lunar_month']} {basic['time_dizhi']}时")
        if basic.get('question'):
            lines.append(f"问题：{basic['question']}")
        lines.append("")
        
        # 卦象结构
        gua_struct = result["gua_structure"]
        ben_gua = gua_struct["ben_gua"]
        
        lines.append("=== 卦象结构分析 ===")
        lines.append(f"本卦：{ben_gua['name']}")
        lines.append(f"├─ 上卦：{ben_gua['shang_gua']['name']}({ben_gua['shang_gua']['wuxing']}) - {ben_gua['shang_gua']['attributes']['象征']} - {ben_gua['shang_gua']['direction']}")
        lines.append(f"└─ 下卦：{ben_gua['xia_gua']['name']}({ben_gua['xia_gua']['wuxing']}) - {ben_gua['xia_gua']['attributes']['象征']} - {ben_gua['xia_gua']['direction']}")
        lines.append("")
        
        # 动爻信息
        dong_yao = ben_gua['dong_yao']
        lines.append(f"动爻：第{dong_yao['position']}爻动 - {dong_yao['yao_nature']}")
        
        # 动爻主旨（根据提示词中的动爻爻辞主旨表）
        yao_zhuzhi = {
            1: "开始、起因、萌芽 - 主始",
            2: "发展、相应、成长 - 主成", 
            3: "高潮、变故、困难 - 主变",
            4: "转机、过渡、迷惑 - 主转",
            5: "权威、核心、成就 - 主极",
            6: "终局、极端、收尾 - 主终"
        }
        lines.append(f"动爻主旨：{yao_zhuzhi.get(dong_yao['position'], '未知')}")
        lines.append("")
        
        # 爻象结构
        yaos = ben_gua['yaos']['structure']
        lines.append("六爻结构（从上到下）：")
        for yao in reversed(yaos):
            marker = " ← 动爻" if yao['position'] == ["初","二","三","四","五","上"][dong_yao['position']-1] else ""
            lines.append(f"{yao['full_position']}：{yao['symbol']} ({yao['value']}){marker}")
        lines.append("")
        
        # 互卦和变卦
        lines.append(f"互卦：{gua_struct['hu_gua']['name']} - 代表内在过程和发展因素")
        lines.append(f"变卦：{gua_struct['bian_gua']['name']} - 代表发展趋势和最终结果")
        
        # 特殊卦象识别
        special_gua = cls._identify_special_gua(ben_gua['name'], gua_struct['hu_gua']['name'], gua_struct['bian_gua']['name'])
        if special_gua:
            lines.append(f"特殊卦象：{special_gua}")
        lines.append("")
        
        # 体用分析（符合提示词要求）
        ti_yong = result["ti_yong_analysis"]
        lines.append("=== 体用分配分析 ===")
        lines.append(f"体卦：{ti_yong['ti_gua']['name']}({ti_yong['ti_gua']['wuxing']}) - 不动者为体，代表求测者自身")
        lines.append(f"用卦：{ti_yong['yong_gua']['name']}({ti_yong['yong_gua']['wuxing']}) - 有动爻者为用，代表所测之事")
        lines.append(f"体用关系：{ti_yong['relation']}")
        lines.append(f"动爻位置：动爻在{ti_yong['dong_yao_position']}")
        lines.append("")
        
        # 五行生克详细分析
        wuxing = result["wuxing_analysis"]
        lines.append("=== 五行生克互动 ===")
        lines.append(f"体卦五行：{wuxing['ti_wuxing']}")
        lines.append(f"用卦五行：{wuxing['yong_wuxing']}")
        lines.append("五行关系分析：")
        for relation_name, relation_value in wuxing['relations'].items():
            relation_desc = cls._get_relation_description(relation_name)
            lines.append(f"  • {relation_desc}：{relation_value}")
        lines.append("")
        
        # 卦气旺衰（符合提示词中的卦气旺衰表）
        season = result["season_analysis"]
        lines.append("=== 卦气旺衰判断 ===")
        lines.append(f"当前时令：{season['season']}季（{season['lunar_month']}月{season['time_dizhi']}时）")
        lines.append(f"体卦{ti_yong['ti_gua']['name']}({wuxing['ti_wuxing']})：{season['ti_gua_strength']['state']} - {season['ti_gua_strength']['description']}")
        lines.append(f"用卦{ti_yong['yong_gua']['name']}({wuxing['yong_wuxing']})：{season['yong_gua_strength']['state']} - {season['yong_gua_strength']['description']}")
        lines.append("")
        
        # 八卦象类信息
        lines.append("=== 八卦象类取象 ===")
        lines.append(f"体卦{ti_yong['ti_gua']['name']}象类：{cls._format_gua_xiangclass(ti_yong['ti_gua']['name'])}")
        lines.append(f"用卦{ti_yong['yong_gua']['name']}象类：{cls._format_gua_xiangclass(ti_yong['yong_gua']['name'])}")
        lines.append("")
        
        lines.append("=== 重要提醒 ===")
        lines.append("请严格按照梅花易数易学推理框架进行分析，")
        lines.append("必须义理象数结合，不可机械套用五行生克公式，")
        lines.append("需要结合八卦象类、事物常理进行综合判断。")
        
        return "\n".join(lines)
    
    @classmethod
    def _identify_special_gua(cls, ben_gua_name: str, hu_gua_name: str, bian_gua_name: str) -> str:
        """识别特殊卦象"""
        # 归魂卦
        guihun_gua = ["火天大有", "天火同人", "地水师", "水地比", "雷泽归妹", "泽雷随", "山风蛊", "风山渐"]
        if ben_gua_name in guihun_gua:
            return f"归魂卦 - {ben_gua_name}属归魂，主不变、回归、稳定，有'归魂不出疆'之象"
        
        # 游魂卦
        youhun_gua = ["火地晋", "雷山小过", "天水讼", "泽风大过", "山雷颐", "地火明夷", "风泽中孚", "水天需"]
        if ben_gua_name in youhun_gua:
            return f"游魂卦 - {ben_gua_name}属游魂，主变动、游离、不安定，有'游魂行千里'之象"
        
        return ""
    
    @classmethod
    def _format_gua_xiangclass(cls, gua_name: str) -> str:
        """格式化八卦象类信息"""
        if gua_name not in BAGUA_ATTRIBUTES:
            return "未知"
        
        attrs = BAGUA_ATTRIBUTES[gua_name]
        wuxing = BAGUA_WUXING[gua_name].value
        direction = BAGUA_DIRECTION[gua_name]
        
        # 构建象类描述
        xiangclass = f"{attrs['象征']}、{attrs['性质']}、{attrs['家庭']}、{attrs['身体']}、{wuxing}、{direction}"
        
        return xiangclass
    
    @classmethod
    def _get_relation_description(cls, relation_name: str) -> str:
        """获取关系描述"""
        descriptions = {
            "ti_yong_relation": "用卦对体卦",
            "hu_shang_to_ti": "互卦上卦对体卦",
            "hu_xia_to_ti": "互卦下卦对体卦",
            "bian_shang_to_ti": "变卦上卦对体卦",
            "bian_xia_to_ti": "变卦下卦对体卦"
        }
        return descriptions.get(relation_name, relation_name)