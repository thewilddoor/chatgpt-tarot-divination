#!/usr/bin/env python3
"""
八字排盘计算器
基于china-testing/bazi项目的专业算法，提供统一的计算接口
"""

import datetime
import sys
import os
import subprocess
import tempfile
from typing import Dict, Any, List

# 添加bazi模块路径
bazi_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bazi')
sys.path.append(bazi_path)

class BaziCalculator:
    """八字排盘计算器主类"""
    
    @classmethod
    def calculate(cls, birth_datetime: datetime.datetime, gender: str = "male", is_lunar: bool = False) -> Dict[str, Any]:
        """
        完整的八字排盘计算
        Args:
            birth_datetime: 出生时间
            gender: 性别 ("male" 或 "female")
            is_lunar: 是否为农历 (默认False使用公历)
        Returns:
            包含完整八字信息的字典
        """
        try:
            # 调用bazi.py程序获取原始输出
            raw_output = cls._run_bazi_program(birth_datetime, gender, is_lunar)
            
            # 解析输出并结构化
            structured_data = cls._parse_bazi_output(raw_output, birth_datetime, gender, is_lunar)
            
            return structured_data
            
        except Exception as e:
            return {
                "error": f"八字排盘计算出错: {str(e)}",
                "success": False
            }
    
    @classmethod
    def _run_bazi_program(cls, birth_datetime: datetime.datetime, gender: str = "male", is_lunar: bool = False) -> str:
        """
        运行bazi.py程序获取八字排盘结果
        """
        bazi_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bazi', 'bazi.py')
        
        # 构建命令参数
        cmd = [
            'python3', bazi_script,
            str(birth_datetime.year),
            str(birth_datetime.month), 
            str(birth_datetime.day),
            str(birth_datetime.hour)
        ]
        
        # 添加选项参数
        if not is_lunar:  # 默认使用公历
            cmd.append('-g')
        if gender == "female":
            cmd.append('-n')
            
        # 运行程序并获取输出
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return result.stdout
            else:
                raise Exception(f"八字程序执行失败: {result.stderr}")
        except subprocess.TimeoutExpired:
            raise Exception("八字程序执行超时")
        except Exception as e:
            raise Exception(f"八字程序执行错误: {str(e)}")
    
    @classmethod
    def _parse_bazi_output(cls, raw_output: str, birth_datetime: datetime.datetime, gender: str, is_lunar: bool) -> Dict[str, Any]:
        """
        解析bazi.py的输出，提取关键信息
        """
        lines = raw_output.strip().split('\n')
        
        # 初始化结果结构
        result = {
            "success": True,
            "basic_info": {
                "birth_datetime": birth_datetime.strftime("%Y年%m月%d日%H时%M分"),
                "gender": "男命" if gender == "male" else "女命",
                "calendar_type": "农历" if is_lunar else "公历"
            },
            "pillars": {
                "year": {},
                "month": {},
                "day": {},
                "hour": {}
            },
            "analysis": {
                "wuxing_scores": {},
                "nayin": {},
                "relationships": {},
                "dayun": [],
                "personality": "",
                "fate_analysis": ""
            },
            "raw_output": raw_output
        }
        
        try:
            # 解析基本排盘信息
            for line in lines:
                line = line.strip()
                # 清理ANSI颜色代码
                import re
                line = re.sub(r'\x1b\[[0-9;]*m', '', line)
                
                # 解析公历农历信息
                if "公历:" in line and "农历:" in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if "公历:" in part and i+1 < len(parts):
                            result["basic_info"]["gregorian_date"] = parts[i+1]
                        if "农历:" in part and i+1 < len(parts):
                            result["basic_info"]["lunar_date"] = parts[i+1]
                
                # 解析四柱信息（查找明确的四柱行）
                if "四柱：" in line:
                    pillars_info = cls._extract_pillars_from_line(line)
                    if pillars_info:
                        result["pillars"] = pillars_info
                
                # 解析五行评分
                if "金:" in line and "木:" in line and "水:" in line:
                    wuxing = cls._extract_wuxing_scores(line)
                    if wuxing:
                        result["analysis"]["wuxing_scores"] = wuxing
                
                # 解析格局信息
                if "格局选用：" in line:
                    result["analysis"]["geju"] = line.replace("格局选用：", "").strip()
                
                # 解析调候信息
                if "调候：" in line:
                    result["analysis"]["diahou"] = line.replace("调候：", "").strip()
            
            # 提取命理分析文本（最后的几段文字）
            fate_lines = []
            personality_lines = []
            
            # 寻找分析文本
            for i, line in enumerate(lines):
                if "《穷通宝鉴》" in line:
                    # 提取穷通宝鉴的内容
                    j = i + 1
                    while j < len(lines) and not lines[j].startswith("《三命通会》"):
                        if lines[j].strip():
                            fate_lines.append(lines[j].strip())
                        j += 1
                
                if "《三命通会》" in line:
                    # 提取三命通会的内容
                    j = i + 1
                    while j < len(lines) and not lines[j].startswith("大运"):
                        if lines[j].strip():
                            fate_lines.append(lines[j].strip())
                        j += 1
            
            result["analysis"]["fate_analysis"] = "\n".join(fate_lines)
            
        except Exception as e:
            result["parsing_warning"] = f"部分解析失败: {str(e)}"
        
        return result
    
    @classmethod
    def _extract_pillars_from_line(cls, line: str) -> Dict[str, Any]:
        """
        从包含四柱信息的行中提取天干地支
        """
        try:
            import re
            
            # 查找四柱：戊子 戊午 庚辰 乙酉 的模式
            # 匹配四柱后面的四个天干地支组合
            pattern = r'四柱：([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥])\s+([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥])\s+([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥])\s+([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥])'
            
            match = re.search(pattern, line)
            if match:
                year_pillar = match.group(1)   # 年柱
                month_pillar = match.group(2)  # 月柱  
                day_pillar = match.group(3)    # 日柱
                hour_pillar = match.group(4)   # 时柱
                
                return {
                    "year": {
                        "天干": year_pillar[0],
                        "地支": year_pillar[1],
                        "柱": year_pillar
                    },
                    "month": {
                        "天干": month_pillar[0],
                        "地支": month_pillar[1], 
                        "柱": month_pillar
                    },
                    "day": {
                        "天干": day_pillar[0],
                        "地支": day_pillar[1],
                        "柱": day_pillar
                    },
                    "hour": {
                        "天干": hour_pillar[0],
                        "地支": hour_pillar[1],
                        "柱": hour_pillar
                    }
                }
            
            return {}
        except Exception as e:
            print(f"解析四柱信息出错: {e}")
            return {}
    
    @classmethod
    def _extract_wuxing_scores(cls, line: str) -> Dict[str, int]:
        """
        提取五行评分
        """
        try:
            wuxing = {}
            import re
            
            # 查找如: 金16  木15  水4  火12  土13 的模式
            pattern = r'([金木水火土])(\d+)'
            matches = re.findall(pattern, line)
            
            for element, score in matches:
                wuxing[element] = int(score)
            
            return wuxing
        except:
            return {}
    
    @classmethod
    def format_for_llm(cls, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        格式化八字排盘结果为AI友好的JSON格式
        """
        if not result.get("success", False):
            return {
                "成功": False,
                "错误": result.get('error', '未知错误')
            }
        
        basic_info = result.get("basic_info", {})
        analysis = result.get("analysis", {})
        pillars = result.get("pillars", {})
        
        # 构建AI友好的结构化JSON数据
        formatted_data = {
            "成功": True,
            "基本信息": {
                "出生时间": basic_info.get('birth_datetime', ''),
                "性别": basic_info.get('gender', ''),
                "历法类型": basic_info.get('calendar_type', ''),
                "公历日期": basic_info.get('gregorian_date', ''),
                "农历日期": basic_info.get('lunar_date', '')
            },
            "四柱": {
                "年柱": pillars.get('year', {}),
                "月柱": pillars.get('month', {}),
                "日柱": pillars.get('day', {}),
                "时柱": pillars.get('hour', {})
            },
            "五行": {
                "评分": analysis.get("wuxing_scores", {}),
                "分析": []
            },
            "格局分析": cls._clean_analysis_text(analysis.get("geju", "")),
            "调候用神": cls._clean_analysis_text(analysis.get("diahou", "")),
            "命理分析": cls._extract_key_fate_insights(analysis.get("fate_analysis", "")),
            "原始输出": cls._clean_raw_output(result.get("raw_output", ""))
        }
        
        # 添加五行力量分析
        if formatted_data['五行']['评分']:
            total_score = sum(formatted_data['五行']['评分'].values())
            for element, score in formatted_data['五行']['评分'].items():
                percentage = (score / total_score * 100) if total_score > 0 else 0
                strength = cls._get_element_strength(percentage)
                formatted_data['五行']['分析'].append({
                    "五行": element,
                    "评分": score,
                    "百分比": round(percentage, 1),
                    "强弱": strength
                })
        
        return formatted_data
    
    @classmethod
    def _clean_analysis_text(cls, text: str) -> str:
        """清理分析文本，去除特殊字符"""
        if not text:
            return ""
        
        import re
        
        # 首先去除ANSI颜色代码
        text = re.sub(r'\x1b\[[0-9;]*m', '', text)
        
        # 去除特殊ASCII字符和符号
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s，。：；！？、（）【】]+', ' ', text)
        
        # 移除多余的空格
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    @classmethod
    def _clean_raw_output(cls, raw_output: str) -> str:
        """清理原始输出，去除ANSI颜色代码"""
        if not raw_output:
            return ""
        
        import re
        # 去除ANSI颜色代码
        cleaned = re.sub(r'\x1b\[[0-9;]*m', '', raw_output)
        return cleaned
    
    @classmethod
    def _get_element_strength(cls, percentage: float) -> str:
        """根据百分比判断五行强弱"""
        if percentage >= 30:
            return "极强"
        elif percentage >= 25:
            return "很强"
        elif percentage >= 20:
            return "较强"
        elif percentage >= 15:
            return "平和"
        elif percentage >= 10:
            return "较弱"
        else:
            return "很弱"
    
    @classmethod
    def _extract_key_fate_insights(cls, fate_text: str) -> str:
        """提取命理分析的关键要点"""
        if not fate_text:
            return ""
        
        # 清理文本
        cleaned_text = cls._clean_analysis_text(fate_text)
        
        # 提取前500字符的关键内容
        if len(cleaned_text) > 500:
            # 寻找句号分割点
            sentences = cleaned_text[:500].split('。')
            if len(sentences) > 1:
                # 保留完整的句子
                key_content = '。'.join(sentences[:-1]) + '。'
            else:
                key_content = cleaned_text[:500]
        else:
            key_content = cleaned_text
        
        return key_content


# 测试函数
def test_bazi_calculator():
    """测试八字排盘计算器"""
    print("=== 八字排盘计算器测试 ===")
    
    # 测试用例：1990年8月17日10时
    test_datetime = datetime.datetime(1990, 8, 17, 10, 0)
    
    result = BaziCalculator.calculate(test_datetime, gender="male", is_lunar=False)
    formatted_output = BaziCalculator.format_for_llm(result)
    
    print(formatted_output)
    print("\n" + "="*50)
    print("✅ 八字排盘计算器测试完成！")


if __name__ == "__main__":
    test_bazi_calculator()