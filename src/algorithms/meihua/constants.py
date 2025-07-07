#!/usr/bin/env python3
"""
梅花易数常量定义
包含八卦、五行、方位等基础数据
"""

from enum import Enum

class WuXing(Enum):
    """五行枚举"""
    METAL = "金"
    WOOD = "木"
    WATER = "水"
    FIRE = "火"
    EARTH = "土"

class SeasonState(Enum):
    """旺相休囚死状态"""
    WANG = "旺"     # 旺 - 最强
    XIANG = "相"    # 相 - 次旺
    XIU = "休"      # 休 - 中等
    QIU = "囚"      # 囚 - 衰弱
    SI = "死"       # 死 - 最弱

# 先天八卦数字对应
XIANTIAN_BAGUA = {
    1: "乾", 2: "兑", 3: "离", 4: "震",
    5: "巽", 6: "坎", 7: "艮", 8: "坤", 0: "坤"
}

# 八卦对应的三爻
BAGUA_YAOS = {
    "乾": [1, 1, 1], "兑": [1, 1, 0], "离": [1, 0, 1], "震": [1, 0, 0],
    "巽": [0, 1, 1], "坎": [0, 1, 0], "艮": [0, 0, 1], "坤": [0, 0, 0]
}

# 八卦五行属性
BAGUA_WUXING = {
    "乾": WuXing.METAL, "兑": WuXing.METAL,
    "离": WuXing.FIRE,
    "震": WuXing.WOOD, "巽": WuXing.WOOD,
    "坎": WuXing.WATER,
    "艮": WuXing.EARTH, "坤": WuXing.EARTH
}

# 八卦方位（后天八卦）
BAGUA_DIRECTION = {
    "坎": "北", "坤": "西南", "震": "东", "巽": "东南",
    "乾": "西北", "兑": "西", "艮": "东北", "离": "南"
}

# 八卦属性
BAGUA_ATTRIBUTES = {
    "乾": {"性质": "刚健", "象征": "天", "家庭": "父", "身体": "头"},
    "坤": {"性质": "柔顺", "象征": "地", "家庭": "母", "身体": "腹"},
    "震": {"性质": "动", "象征": "雷", "家庭": "长男", "身体": "足"},
    "巽": {"性质": "入", "象征": "风", "家庭": "长女", "身体": "股"},
    "坎": {"性质": "陷", "象征": "水", "家庭": "中男", "身体": "耳"},
    "离": {"性质": "丽", "象征": "火", "家庭": "中女", "身体": "目"},
    "艮": {"性质": "止", "象征": "山", "家庭": "少男", "身体": "手"},
    "兑": {"性质": "悦", "象征": "泽", "家庭": "少女", "身体": "口"}
}

# 六十四卦名表
LIUSHI_SIGUA = {
    "乾乾": "乾为天", "乾兑": "天泽履", "乾离": "天火同人", "乾震": "天雷无妄",
    "乾巽": "天风姤", "乾坎": "天水讼", "乾艮": "天山遁", "乾坤": "天地否",
    "兑乾": "泽天夬", "兑兑": "兑为泽", "兑离": "泽火革", "兑震": "泽雷随",
    "兑巽": "泽风大过", "兑坎": "泽水困", "兑艮": "泽山咸", "兑坤": "泽地萃",
    "离乾": "火天大有", "离兑": "火泽睽", "离离": "离为火", "离震": "火雷噬嗑",
    "离巽": "火风鼎", "离坎": "火水未济", "离艮": "火山旅", "离坤": "火地晋",
    "震乾": "雷天大壮", "震兑": "雷泽归妹", "震离": "雷火丰", "震震": "震为雷",
    "震巽": "雷风恒", "震坎": "雷水解", "震艮": "雷山小过", "震坤": "雷地豫",
    "巽乾": "风天小畜", "巽兑": "风泽中孚", "巽离": "风火家人", "巽震": "风雷益",
    "巽巽": "巽为风", "巽坎": "风水涣", "巽艮": "风山渐", "巽坤": "风地观",
    "坎乾": "水天需", "坎兑": "水泽节", "坎离": "水火既济", "坎震": "水雷屯",
    "坎巽": "水风井", "坎坎": "坎为水", "坎艮": "水山蹇", "坎坤": "水地比",
    "艮乾": "山天大畜", "艮兑": "山泽损", "艮离": "山火贲", "艮震": "山雷颐",
    "艮巽": "山风蛊", "艮坎": "山水蒙", "艮艮": "艮为山", "艮坤": "山地剥",
    "坤乾": "地天泰", "坤兑": "地泽临", "坤离": "地火明夷", "坤震": "地雷复",
    "坤巽": "地风升", "坤坎": "地水师", "坤艮": "地山谦", "坤坤": "坤为地"
}

# 十二地支
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 地支对应的时辰
DIZHI_HOURS = {
    "子": (23, 1), "丑": (1, 3), "寅": (3, 5), "卯": (5, 7),
    "辰": (7, 9), "巳": (9, 11), "午": (11, 13), "未": (13, 15),
    "申": (15, 17), "酉": (17, 19), "戌": (19, 21), "亥": (21, 23)
}

# 各五行在四季的旺相休囚死状态
SEASON_STRENGTH = {
    "春": {WuXing.WOOD: SeasonState.WANG, WuXing.FIRE: SeasonState.XIANG, 
          WuXing.WATER: SeasonState.XIU, WuXing.METAL: SeasonState.QIU, WuXing.EARTH: SeasonState.SI},
    "夏": {WuXing.FIRE: SeasonState.WANG, WuXing.EARTH: SeasonState.XIANG,
          WuXing.WOOD: SeasonState.XIU, WuXing.WATER: SeasonState.QIU, WuXing.METAL: SeasonState.SI},
    "秋": {WuXing.METAL: SeasonState.WANG, WuXing.WATER: SeasonState.XIANG,
          WuXing.EARTH: SeasonState.XIU, WuXing.FIRE: SeasonState.QIU, WuXing.WOOD: SeasonState.SI},
    "冬": {WuXing.WATER: SeasonState.WANG, WuXing.WOOD: SeasonState.XIANG,
          WuXing.METAL: SeasonState.XIU, WuXing.EARTH: SeasonState.QIU, WuXing.FIRE: SeasonState.SI}
}