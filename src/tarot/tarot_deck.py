# -*- coding: utf-8 -*-
"""
塔罗牌牌库数据
基于Rider-Waite-Smith塔罗牌系统，包含完整的78张塔罗牌
"""

# 大阿卡纳牌（22张）
MAJOR_ARCANA = [
    {
        "name": "The Fool",
        "name_zh": "愚者",
        "number": 0,
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "新开始、纯真、冒险、自发性",
        "reversed_meaning": "鲁莽、风险、愚蠢、冲动",
        "description": "愚者代表新的开始和纯真的冒险精神，踏上未知的旅程。"
    },
    {
        "name": "The Magician",
        "name_zh": "魔术师",
        "number": 1,
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "意志力、能力、专注、掌控",
        "reversed_meaning": "缺乏专注、意志薄弱、欺骗",
        "description": "魔术师象征着将想法转化为现实的能力和强大的意志力。"
    },
    {
        "name": "The High Priestess",
        "name_zh": "女祭司",
        "number": 2,
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "直觉、神秘、潜意识、内在智慧",
        "reversed_meaning": "忽视直觉、表面化、缺乏洞察",
        "description": "女祭司代表内在的智慧和直觉，守护着神秘的知识。"
    },
    {
        "name": "The Empress",
        "name_zh": "皇后",
        "number": 3,
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "丰饶、创造、母性、自然",
        "reversed_meaning": "创意枯竭、依赖、无私奉献过度",
        "description": "皇后象征着丰饶、创造力和母性的爱。"
    },
    {
        "name": "The Emperor",
        "name_zh": "皇帝",
        "number": 4,
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "权威、结构、控制、父性",
        "reversed_meaning": "专制、缺乏纪律、灵活性不足",
        "description": "皇帝代表权威、秩序和结构化的力量。"
    },
    {
        "name": "The Hierophant",
        "name_zh": "教皇",
        "number": 5,
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "传统、精神指导、制度、学习",
        "reversed_meaning": "反叛、标新立异、自由思想",
        "description": "教皇象征着传统智慧和精神指导。"
    },
    {
        "name": "The Lovers",
        "name_zh": "恋人",
        "number": 6,
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "爱情、选择、伙伴关系、价值观",
        "reversed_meaning": "关系破裂、价值冲突、不忠",
        "description": "恋人代表爱情、选择和重要的关系。"
    },
    {
        "name": "The Chariot",
        "name_zh": "战车",
        "number": 7,
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "控制、意志力、成功、决心",
        "reversed_meaning": "缺乏控制、缺乏方向、侵略性",
        "description": "战车象征着通过意志力和控制获得成功。"
    },
    {
        "name": "Strength",
        "name_zh": "力量",
        "number": 8,
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "内在力量、勇气、耐心、控制",
        "reversed_meaning": "内在恐惧、自我怀疑、缺乏信心",
        "description": "力量代表内在的勇气和温柔的控制。"
    },
    {
        "name": "The Hermit",
        "name_zh": "隐者",
        "number": 9,
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "内省、寻找真理、内在指导、孤独",
        "reversed_meaning": "孤立、迷失、拒绝帮助",
        "description": "隐者象征着内在的搜索和精神指导。"
    },
    {
        "name": "Wheel of Fortune",
        "name_zh": "命运之轮",
        "number": 10,
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "运气、命运、转折点、周期",
        "reversed_meaning": "厄运、缺乏控制、破环的循环",
        "description": "命运之轮代表命运的转折和生命的周期性。"
    },
    {
        "name": "Justice",
        "name_zh": "正义",
        "number": 11,
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "公正、真理、法律、业力",
        "reversed_meaning": "不公、不诚实、缺乏问责",
        "description": "正义象征着公平、真理和道德平衡。"
    },
    {
        "name": "The Hanged Man",
        "name_zh": "倒吊人",
        "number": 12,
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "暂停、释放、牺牲、新的视角",
        "reversed_meaning": "拖延、抗拒、无意义的牺牲",
        "description": "倒吊人代表暂停和从新角度看待问题。"
    },
    {
        "name": "Death",
        "name_zh": "死神",
        "number": 13,
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "结束、转变、重生、过渡",
        "reversed_meaning": "抗拒改变、停滞、腐朽",
        "description": "死神象征着结束和重新开始的转变。"
    },
    {
        "name": "Temperance",
        "name_zh": "节制",
        "number": 14,
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "平衡、调和、耐心、目标",
        "reversed_meaning": "不平衡、过度、缺乏长期愿景",
        "description": "节制代表平衡、调和和中庸之道。"
    },
    {
        "name": "The Devil",
        "name_zh": "恶魔",
        "number": 15,
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "束缚、成瘾、性、物质主义",
        "reversed_meaning": "释放、打破束缚、重获自由",
        "description": "恶魔象征着诱惑、束缚和物质的陷阱。"
    },
    {
        "name": "The Tower",
        "name_zh": "塔",
        "number": 16,
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "突然的改变、破坏、启示、觉醒",
        "reversed_meaning": "避免灾难、恐惧改变、延迟不可避免",
        "description": "塔代表突然的破坏和令人震惊的启示。"
    },
    {
        "name": "The Star",
        "name_zh": "星星",
        "number": 17,
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "希望、信仰、灵感、指导",
        "reversed_meaning": "绝望、信仰丧失、缺乏灵感",
        "description": "星星象征着希望、信仰和精神指导。"
    },
    {
        "name": "The Moon",
        "name_zh": "月亮",
        "number": 18,
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "幻觉、恐惧、焦虑、潜意识",
        "reversed_meaning": "释放恐惧、现实、直觉",
        "description": "月亮代表幻觉、恐惧和潜意识的迷雾。"
    },
    {
        "name": "The Sun",
        "name_zh": "太阳",
        "number": 19,
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "快乐、成功、乐观、活力",
        "reversed_meaning": "暂时的挫折、缺乏成功、悲观",
        "description": "太阳象征着快乐、成功和生命的活力。"
    },
    {
        "name": "Judgement",
        "name_zh": "审判",
        "number": 20,
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "反思、内在召唤、宽恕、重生",
        "reversed_meaning": "自我怀疑、缺乏自省、严厉的自我评判",
        "description": "审判代表反思、内在的召唤和精神的重生。"
    },
    {
        "name": "The World",
        "name_zh": "世界",
        "number": 21,
        "arcana": "Major Arcana",
        "suit": None,
        "upright_meaning": "成就、完成、旅程的结束、满足",
        "reversed_meaning": "不完整、缺乏闭合、停滞",
        "description": "世界象征着成就、完成和生命周期的圆满。"
    }
]

# 小阿卡纳牌 - 权杖（火元素）
WANDS_CARDS = [
    {
        "name": "Ace of Wands",
        "name_zh": "权杖王牌",
        "number": 1,
        "arcana": "Minor Arcana",
        "suit": "Wands",
        "element": "Fire",
        "upright_meaning": "创造、新的开始、灵感、潜力",
        "reversed_meaning": "缺乏能量、延迟、错误的开始",
        "description": "权杖王牌代表创造力和新项目的开始。"
    },
    {
        "name": "Two of Wands",
        "name_zh": "权杖二",
        "number": 2,
        "arcana": "Minor Arcana",
        "suit": "Wands",
        "element": "Fire",
        "upright_meaning": "规划、预见、个人权力、控制",
        "reversed_meaning": "缺乏规划、自我怀疑、没有控制",
        "description": "权杖二象征着计划和对未来的展望。"
    },
    {
        "name": "Three of Wands",
        "name_zh": "权杖三",
        "number": 3,
        "arcana": "Minor Arcana",
        "suit": "Wands",
        "element": "Fire",
        "upright_meaning": "扩展、预见、领导力、贸易",
        "reversed_meaning": "缺乏预见、延迟、障碍",
        "description": "权杖三代表扩展和远见。"
    },
    {
        "name": "Four of Wands",
        "name_zh": "权杖四",
        "number": 4,
        "arcana": "Minor Arcana",
        "suit": "Wands",
        "element": "Fire",
        "upright_meaning": "庆祝、和谐、家庭、稳定",
        "reversed_meaning": "缺乏支持、不稳定、家庭冲突",
        "description": "权杖四象征着庆祝和家庭和谐。"
    },
    {
        "name": "Five of Wands",
        "name_zh": "权杖五",
        "number": 5,
        "arcana": "Minor Arcana",
        "suit": "Wands",
        "element": "Fire",
        "upright_meaning": "冲突、竞争、紧张、分歧",
        "reversed_meaning": "避免冲突、内在冲突、释放紧张",
        "description": "权杖五代表冲突和竞争。"
    },
    {
        "name": "Six of Wands",
        "name_zh": "权杖六",
        "number": 6,
        "arcana": "Minor Arcana",
        "suit": "Wands",
        "element": "Fire",
        "upright_meaning": "成功、认可、胜利、公众赞扬",
        "reversed_meaning": "私人成就、自我怀疑、缺乏认可",
        "description": "权杖六象征着成功和公众认可。"
    },
    {
        "name": "Seven of Wands",
        "name_zh": "权杖七",
        "number": 7,
        "arcana": "Minor Arcana",
        "suit": "Wands",
        "element": "Fire",
        "upright_meaning": "挑战、竞争、保护、毅力",
        "reversed_meaning": "精疲力竭、放弃、缺乏勇气",
        "description": "权杖七代表坚持立场和防御。"
    },
    {
        "name": "Eight of Wands",
        "name_zh": "权杖八",
        "number": 8,
        "arcana": "Minor Arcana",
        "suit": "Wands",
        "element": "Fire",
        "upright_meaning": "快速行动、进展、变化、消息",
        "reversed_meaning": "延迟、挫折、缺乏进展",
        "description": "权杖八象征着快速的行动和进展。"
    },
    {
        "name": "Nine of Wands",
        "name_zh": "权杖九",
        "number": 9,
        "arcana": "Minor Arcana",
        "suit": "Wands",
        "element": "Fire",
        "upright_meaning": "弹性、坚持、测试信念、边界",
        "reversed_meaning": "固执、偏执、防御过度",
        "description": "权杖九代表坚韧和最后的坚持。"
    },
    {
        "name": "Ten of Wands",
        "name_zh": "权杖十",
        "number": 10,
        "arcana": "Minor Arcana",
        "suit": "Wands",
        "element": "Fire",
        "upright_meaning": "负担、压力、辛勤工作、责任",
        "reversed_meaning": "释放负担、委派、寻求支持",
        "description": "权杖十象征着承担重担和责任。"
    },
    {
        "name": "Page of Wands",
        "name_zh": "权杖侍从",
        "number": 11,
        "arcana": "Minor Arcana",
        "suit": "Wands",
        "element": "Fire",
        "upright_meaning": "灵感、想法、学习、发现",
        "reversed_meaning": "缺乏方向、拖延、缺乏计划",
        "description": "权杖侍从代表新的灵感和学习的热情。"
    },
    {
        "name": "Knight of Wands",
        "name_zh": "权杖骑士",
        "number": 12,
        "arcana": "Minor Arcana",
        "suit": "Wands",
        "element": "Fire",
        "upright_meaning": "行动、冲动、冒险、能量",
        "reversed_meaning": "鲁莽、缺乏耐心、冲动的行为",
        "description": "权杖骑士象征着冲动的行动和冒险精神。"
    },
    {
        "name": "Queen of Wands",
        "name_zh": "权杖皇后",
        "number": 13,
        "arcana": "Minor Arcana",
        "suit": "Wands",
        "element": "Fire",
        "upright_meaning": "自信、独立、社交、决心",
        "reversed_meaning": "自私、嫉妒、不安全感",
        "description": "权杖皇后代表自信和独立的精神。"
    },
    {
        "name": "King of Wands",
        "name_zh": "权杖国王",
        "number": 14,
        "arcana": "Minor Arcana",
        "suit": "Wands",
        "element": "Fire",
        "upright_meaning": "领导力、愿景、企业家精神、荣誉",
        "reversed_meaning": "专制、冲动、残酷、无情",
        "description": "权杖国王象征着领导力和企业家精神。"
    }
]

# 小阿卡纳牌 - 圣杯（水元素）
CUPS_CARDS = [
    {
        "name": "Ace of Cups",
        "name_zh": "圣杯王牌",
        "number": 1,
        "arcana": "Minor Arcana",
        "suit": "Cups",
        "element": "Water",
        "upright_meaning": "新的爱情、直觉、精神、创造力",
        "reversed_meaning": "情感封闭、压抑的感情、创意枯竭",
        "description": "圣杯王牌代表新的情感开始和精神觉醒。"
    },
    {
        "name": "Two of Cups",
        "name_zh": "圣杯二",
        "number": 2,
        "arcana": "Minor Arcana",
        "suit": "Cups",
        "element": "Water",
        "upright_meaning": "伙伴关系、爱情、互相吸引、关系",
        "reversed_meaning": "破裂的关系、不平衡、缺乏信任",
        "description": "圣杯二象征着爱情和伙伴关系。"
    },
    {
        "name": "Three of Cups",
        "name_zh": "圣杯三",
        "number": 3,
        "arcana": "Minor Arcana",
        "suit": "Cups",
        "element": "Water",
        "upright_meaning": "友谊、社区、庆祝、创造力",
        "reversed_meaning": "孤立、孤独、团队冲突",
        "description": "圣杯三代表友谊和社会联系。"
    },
    {
        "name": "Four of Cups",
        "name_zh": "圣杯四",
        "number": 4,
        "arcana": "Minor Arcana",
        "suit": "Cups",
        "element": "Water",
        "upright_meaning": "冷漠、沉思、无聊、错过机会",
        "reversed_meaning": "动机、重燃兴趣、寻求目标",
        "description": "圣杯四象征着冷漠和错过的机会。"
    },
    {
        "name": "Five of Cups",
        "name_zh": "圣杯五",
        "number": 5,
        "arcana": "Minor Arcana",
        "suit": "Cups",
        "element": "Water",
        "upright_meaning": "损失、后悔、悲伤、悼念",
        "reversed_meaning": "接受、向前看、寻找支持",
        "description": "圣杯五代表损失和悲伤。"
    },
    {
        "name": "Six of Cups",
        "name_zh": "圣杯六",
        "number": 6,
        "arcana": "Minor Arcana",
        "suit": "Cups",
        "element": "Water",
        "upright_meaning": "怀旧、童年记忆、纯真、团聚",
        "reversed_meaning": "被过去束缚、缺乏现实感、不成熟",
        "description": "圣杯六象征着怀旧和童年的纯真。"
    },
    {
        "name": "Seven of Cups",
        "name_zh": "圣杯七",
        "number": 7,
        "arcana": "Minor Arcana",
        "suit": "Cups",
        "element": "Water",
        "upright_meaning": "幻想、选择、愿望思维、分心",
        "reversed_meaning": "决定、意志力、专注、排定优先级",
        "description": "圣杯七代表选择和幻想。"
    },
    {
        "name": "Eight of Cups",
        "name_zh": "圣杯八",
        "number": 8,
        "arcana": "Minor Arcana",
        "suit": "Cups",
        "element": "Water",
        "upright_meaning": "放弃、寻找更深的意义、离开",
        "reversed_meaning": "恐惧改变、避免更深的工作、缺乏勇气",
        "description": "圣杯八象征着放弃和寻找更深层的意义。"
    },
    {
        "name": "Nine of Cups",
        "name_zh": "圣杯九",
        "number": 9,
        "arcana": "Minor Arcana",
        "suit": "Cups",
        "element": "Water",
        "upright_meaning": "满足、情感满足、奢侈、成功",
        "reversed_meaning": "内在幸福、物质主义、不满",
        "description": "圣杯九代表满足和情感上的成功。"
    },
    {
        "name": "Ten of Cups",
        "name_zh": "圣杯十",
        "number": 10,
        "arcana": "Minor Arcana",
        "suit": "Cups",
        "element": "Water",
        "upright_meaning": "家庭幸福、情感满足、和谐、对齐",
        "reversed_meaning": "家庭冲突、价值观不一致、缺乏支持",
        "description": "圣杯十象征着家庭幸福和完美的和谐。"
    },
    {
        "name": "Page of Cups",
        "name_zh": "圣杯侍从",
        "number": 11,
        "arcana": "Minor Arcana",
        "suit": "Cups",
        "element": "Water",
        "upright_meaning": "创意机会、直觉消息、好奇心、新的可能性",
        "reversed_meaning": "情感不成熟、创意封闭、缺乏直觉",
        "description": "圣杯侍从代表创意和直觉的讯息。"
    },
    {
        "name": "Knight of Cups",
        "name_zh": "圣杯骑士",
        "number": 12,
        "arcana": "Minor Arcana",
        "suit": "Cups",
        "element": "Water",
        "upright_meaning": "浪漫、魅力、想象力、艺术",
        "reversed_meaning": "情绪化、喜怒无常、缺乏目标",
        "description": "圣杯骑士象征着浪漫和艺术气质。"
    },
    {
        "name": "Queen of Cups",
        "name_zh": "圣杯皇后",
        "number": 13,
        "arcana": "Minor Arcana",
        "suit": "Cups",
        "element": "Water",
        "upright_meaning": "同情心、关怀、情感安全、直觉",
        "reversed_meaning": "情感不稳定、依赖、自私",
        "description": "圣杯皇后代表同情心和情感的智慧。"
    },
    {
        "name": "King of Cups",
        "name_zh": "圣杯国王",
        "number": 14,
        "arcana": "Minor Arcana",
        "suit": "Cups",
        "element": "Water",
        "upright_meaning": "情感平衡、同情心、外交、控制",
        "reversed_meaning": "情感操控、喜怒无常、缺乏同情心",
        "description": "圣杯国王象征着情感的成熟和控制。"
    }
]

# 小阿卡纳牌 - 宝剑（风元素）
SWORDS_CARDS = [
    {
        "name": "Ace of Swords",
        "name_zh": "宝剑王牌",
        "number": 1,
        "arcana": "Minor Arcana",
        "suit": "Swords",
        "element": "Air",
        "upright_meaning": "新想法、心理清晰、沟通、真理",
        "reversed_meaning": "混乱、残酷、混乱的想法",
        "description": "宝剑王牌代表新的想法和心理上的突破。"
    },
    {
        "name": "Two of Swords",
        "name_zh": "宝剑二",
        "number": 2,
        "arcana": "Minor Arcana",
        "suit": "Swords",
        "element": "Air",
        "upright_meaning": "困难的选择、权衡、僵局、否认",
        "reversed_meaning": "优柔寡断、困惑、信息过载",
        "description": "宝剑二象征着困难的决定和内心的冲突。"
    },
    {
        "name": "Three of Swords",
        "name_zh": "宝剑三",
        "number": 3,
        "arcana": "Minor Arcana",
        "suit": "Swords",
        "element": "Air",
        "upright_meaning": "心碎、痛苦、悲伤、拒绝",
        "reversed_meaning": "恢复、宽恕、向前看",
        "description": "宝剑三代表心碎和深深的悲伤。"
    },
    {
        "name": "Four of Swords",
        "name_zh": "宝剑四",
        "number": 4,
        "arcana": "Minor Arcana",
        "suit": "Swords",
        "element": "Air",
        "upright_meaning": "休息、恢复、沉思、孤独",
        "reversed_meaning": "精疲力竭、倦怠、深度抑郁",
        "description": "宝剑四象征着休息和恢复的需要。"
    },
    {
        "name": "Five of Swords",
        "name_zh": "宝剑五",
        "number": 5,
        "arcana": "Minor Arcana",
        "suit": "Swords",
        "element": "Air",
        "upright_meaning": "冲突、不和、失败、背叛",
        "reversed_meaning": "和解、化解冲突、宽恕",
        "description": "宝剑五代表冲突和不公平的胜利。"
    },
    {
        "name": "Six of Swords",
        "name_zh": "宝剑六",
        "number": 6,
        "arcana": "Minor Arcana",
        "suit": "Swords",
        "element": "Air",
        "upright_meaning": "过渡、改变、前进、释放",
        "reversed_meaning": "个人过渡、抗拒改变、无法释放",
        "description": "宝剑六象征着从困难中走出。"
    },
    {
        "name": "Seven of Swords",
        "name_zh": "宝剑七",
        "number": 7,
        "arcana": "Minor Arcana",
        "suit": "Swords",
        "element": "Air",
        "upright_meaning": "欺骗、策略、逃避、不诚实",
        "reversed_meaning": "承认、诚实、悔改",
        "description": "宝剑七代表欺骗和逃避。"
    },
    {
        "name": "Eight of Swords",
        "name_zh": "宝剑八",
        "number": 8,
        "arcana": "Minor Arcana",
        "suit": "Swords",
        "element": "Air",
        "upright_meaning": "限制、陷阱、受害者心态、自我限制",
        "reversed_meaning": "自我接受、新的视角、释放",
        "description": "宝剑八象征着自我施加的限制。"
    },
    {
        "name": "Nine of Swords",
        "name_zh": "宝剑九",
        "number": 9,
        "arcana": "Minor Arcana",
        "suit": "Swords",
        "element": "Air",
        "upright_meaning": "焦虑、担心、恐惧、噩梦",
        "reversed_meaning": "内在恐惧、释放焦虑、寻求帮助",
        "description": "宝剑九代表深深的焦虑和恐惧。"
    },
    {
        "name": "Ten of Swords",
        "name_zh": "宝剑十",
        "number": 10,
        "arcana": "Minor Arcana",
        "suit": "Swords",
        "element": "Air",
        "upright_meaning": "背叛、结束、损失、崩溃",
        "reversed_meaning": "恢复、重生、抗拒结束",
        "description": "宝剑十象征着痛苦的结束和背叛。"
    },
    {
        "name": "Page of Swords",
        "name_zh": "宝剑侍从",
        "number": 11,
        "arcana": "Minor Arcana",
        "suit": "Swords",
        "element": "Air",
        "upright_meaning": "好奇心、警觉、精神能量、新想法",
        "reversed_meaning": "散布谣言、间谍活动、欺骗",
        "description": "宝剑侍从代表好奇心和新的思想。"
    },
    {
        "name": "Knight of Swords",
        "name_zh": "宝剑骑士",
        "number": 12,
        "arcana": "Minor Arcana",
        "suit": "Swords",
        "element": "Air",
        "upright_meaning": "雄心、行动、驱动力、快速思考",
        "reversed_meaning": "鲁莽、冲动、缺乏计划",
        "description": "宝剑骑士象征着雄心和快速的行动。"
    },
    {
        "name": "Queen of Swords",
        "name_zh": "宝剑皇后",
        "number": 13,
        "arcana": "Minor Arcana",
        "suit": "Swords",
        "element": "Air",
        "upright_meaning": "独立、理性思维、清晰、直接",
        "reversed_meaning": "过度情绪化、严厉、苦涩",
        "description": "宝剑皇后代表独立和理性的思维。"
    },
    {
        "name": "King of Swords",
        "name_zh": "宝剑国王",
        "number": 14,
        "arcana": "Minor Arcana",
        "suit": "Swords",
        "element": "Air",
        "upright_meaning": "权威、理性、智力、真理",
        "reversed_meaning": "专制、滥用权力、缺乏同情心",
        "description": "宝剑国王象征着理性的权威和公正。"
    }
]

# 小阿卡纳牌 - 钱币（土元素）
PENTACLES_CARDS = [
    {
        "name": "Ace of Pentacles",
        "name_zh": "钱币王牌",
        "number": 1,
        "arcana": "Minor Arcana",
        "suit": "Pentacles",
        "element": "Earth",
        "upright_meaning": "新的财务机会、现实、实用性",
        "reversed_meaning": "错失机会、缺乏规划、不良投资",
        "description": "钱币王牌代表新的物质机会和实际的开始。"
    },
    {
        "name": "Two of Pentacles",
        "name_zh": "钱币二",
        "number": 2,
        "arcana": "Minor Arcana",
        "suit": "Pentacles",
        "element": "Earth",
        "upright_meaning": "多重任务、时间管理、优先级、适应性",
        "reversed_meaning": "杂乱无章、缺乏组织、超负荷",
        "description": "钱币二象征着平衡多重责任。"
    },
    {
        "name": "Three of Pentacles",
        "name_zh": "钱币三",
        "number": 3,
        "arcana": "Minor Arcana",
        "suit": "Pentacles",
        "element": "Earth",
        "upright_meaning": "团队合作、协作、学习、实施",
        "reversed_meaning": "缺乏团队合作、无效率、缺乏技能",
        "description": "钱币三代表团队合作和技能建设。"
    },
    {
        "name": "Four of Pentacles",
        "name_zh": "钱币四",
        "number": 4,
        "arcana": "Minor Arcana",
        "suit": "Pentacles",
        "element": "Earth",
        "upright_meaning": "储蓄、安全、保守主义、稀缺",
        "reversed_meaning": "过度消费、慷慨、共享财富",
        "description": "钱币四象征着物质安全和保守。"
    },
    {
        "name": "Five of Pentacles",
        "name_zh": "钱币五",
        "number": 5,
        "arcana": "Minor Arcana",
        "suit": "Pentacles",
        "element": "Earth",
        "upright_meaning": "财务损失、贫困、缺乏、孤立",
        "reversed_meaning": "恢复、改善、寻求帮助",
        "description": "钱币五代表财务困难和需要帮助。"
    },
    {
        "name": "Six of Pentacles",
        "name_zh": "钱币六",
        "number": 6,
        "arcana": "Minor Arcana",
        "suit": "Pentacles",
        "element": "Earth",
        "upright_meaning": "慷慨、施舍、分享、公平",
        "reversed_meaning": "自私、债务、单方面援助",
        "description": "钱币六象征着慷慨和公平的交换。"
    },
    {
        "name": "Seven of Pentacles",
        "name_zh": "钱币七",
        "number": 7,
        "arcana": "Minor Arcana",
        "suit": "Pentacles",
        "element": "Earth",
        "upright_meaning": "投资、辛勤工作、耐心、坚持",
        "reversed_meaning": "缺乏进展、返工、不耐烦",
        "description": "钱币七代表长期投资和耐心等待。"
    },
    {
        "name": "Eight of Pentacles",
        "name_zh": "钱币八",
        "number": 8,
        "arcana": "Minor Arcana",
        "suit": "Pentacles",
        "element": "Earth",
        "upright_meaning": "学徒制、技能发展、专注、详细",
        "reversed_meaning": "缺乏专注、完美主义、技能不足",
        "description": "钱币八象征着技能的精进和专注。"
    },
    {
        "name": "Nine of Pentacles",
        "name_zh": "钱币九",
        "number": 9,
        "arcana": "Minor Arcana",
        "suit": "Pentacles",
        "element": "Earth",
        "upright_meaning": "独立、财务安全、自给自足、奢侈",
        "reversed_meaning": "依赖、财务挫折、缺乏自立",
        "description": "钱币九代表独立和财务自由。"
    },
    {
        "name": "Ten of Pentacles",
        "name_zh": "钱币十",
        "number": 10,
        "arcana": "Minor Arcana",
        "suit": "Pentacles",
        "element": "Earth",
        "upright_meaning": "财富、财务安全、家庭、传承",
        "reversed_meaning": "财务损失、缺乏稳定、家庭冲突",
        "description": "钱币十象征着财富和家庭的稳定。"
    },
    {
        "name": "Page of Pentacles",
        "name_zh": "钱币侍从",
        "number": 11,
        "arcana": "Minor Arcana",
        "suit": "Pentacles",
        "element": "Earth",
        "upright_meaning": "学习、新机会、野心、实用性",
        "reversed_meaning": "缺乏进展、拖延、缺乏承诺",
        "description": "钱币侍从代表学习新技能和实际机会。"
    },
    {
        "name": "Knight of Pentacles",
        "name_zh": "钱币骑士",
        "number": 12,
        "arcana": "Minor Arcana",
        "suit": "Pentacles",
        "element": "Earth",
        "upright_meaning": "效率、辛勤工作、责任感、常规",
        "reversed_meaning": "自满、缺乏进展、完美主义",
        "description": "钱币骑士象征着勤勉和可靠性。"
    },
    {
        "name": "Queen of Pentacles",
        "name_zh": "钱币皇后",
        "number": 13,
        "arcana": "Minor Arcana",
        "suit": "Pentacles",
        "element": "Earth",
        "upright_meaning": "养育、实用性、提供、安全",
        "reversed_meaning": "物质主义、自私、工作失衡",
        "description": "钱币皇后代表养育和实际的关怀。"
    },
    {
        "name": "King of Pentacles",
        "name_zh": "钱币国王",
        "number": 14,
        "arcana": "Minor Arcana",
        "suit": "Pentacles",
        "element": "Earth",
        "upright_meaning": "财务成功、企业、领导力、安全",
        "reversed_meaning": "贪婪、物质主义、财务失败",
        "description": "钱币国王象征着财务成功和稳固的领导。"
    }
]

# 完整的78张塔罗牌
FULL_TAROT_DECK = MAJOR_ARCANA + WANDS_CARDS + CUPS_CARDS + SWORDS_CARDS + PENTACLES_CARDS

# 三牌阵位置含义
THREE_CARD_SPREAD_POSITIONS = [
    {
        "position": 1,
        "meaning": "过去/原因",
        "description": "影响当前情况的过去事件或根本原因"
    },
    {
        "position": 2,
        "meaning": "现在/当前状态",
        "description": "当前的情况、挑战或机遇"
    },
    {
        "position": 3,
        "meaning": "未来/结果",
        "description": "可能的结果或建议的行动方向"
    }
]

def get_card_by_name(card_name: str):
    """根据卡牌名称获取卡牌信息"""
    for card in FULL_TAROT_DECK:
        if card["name"] == card_name or card["name_zh"] == card_name:
            return card
    return None

def get_cards_by_suit(suit: str):
    """获取指定花色的所有卡牌"""
    return [card for card in FULL_TAROT_DECK if card["suit"] == suit]

def get_major_arcana():
    """获取所有大阿卡纳牌"""
    return MAJOR_ARCANA

def get_minor_arcana():
    """获取所有小阿卡纳牌"""
    return [card for card in FULL_TAROT_DECK if card["arcana"] == "Minor Arcana"]