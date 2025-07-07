# -*- coding: utf-8 -*-
"""
塔罗牌抽牌算法
实现Fisher-Yates洗牌算法和各种牌阵的抽牌逻辑
"""

import random
import copy
from typing import List, Dict, Any, Optional
from .tarot_deck import FULL_TAROT_DECK, THREE_CARD_SPREAD_POSITIONS


class TarotCardDrawer:
    """塔罗牌抽牌器"""
    
    def __init__(self, seed: Optional[int] = None):
        """
        初始化抽牌器
        :param seed: 随机种子，用于测试时保证结果一致
        """
        if seed is not None:
            random.seed(seed)
        self.deck = copy.deepcopy(FULL_TAROT_DECK)
        self.shuffled_deck = []
        self.drawn_cards = []
    
    def fisher_yates_shuffle(self, deck: List[Dict]) -> List[Dict]:
        """
        Fisher-Yates洗牌算法
        确保每种排列的概率相等
        """
        shuffled = copy.deepcopy(deck)
        n = len(shuffled)
        
        # 从最后一个元素开始向前遍历
        for i in range(n - 1, 0, -1):
            # 生成0到i之间的随机索引
            j = random.randint(0, i)
            # 交换元素
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
        
        return shuffled
    
    def shuffle_deck(self):
        """洗牌"""
        self.shuffled_deck = self.fisher_yates_shuffle(self.deck)
        self.drawn_cards = []
    
    def draw_single_card(self) -> Dict[str, Any]:
        """
        抽取单张塔罗牌
        :return: 包含牌面信息和正逆位的字典
        """
        if not self.shuffled_deck:
            self.shuffle_deck()
        
        if len(self.drawn_cards) >= len(self.shuffled_deck):
            raise ValueError("牌库已空，无法继续抽牌")
        
        # 抽取下一张牌
        card = self.shuffled_deck[len(self.drawn_cards)]
        
        # 随机决定正逆位（50%概率）
        is_reversed = random.choice([True, False])
        
        # 构建抽牌结果
        drawn_card = {
            **card,
            "is_reversed": is_reversed,
            "orientation": "逆位" if is_reversed else "正位",
            "meaning": card["reversed_meaning"] if is_reversed else card["upright_meaning"],
            "draw_order": len(self.drawn_cards) + 1
        }
        
        self.drawn_cards.append(drawn_card)
        return drawn_card
    
    def draw_three_card_spread(self, positions: Optional[List[int]] = None) -> Dict[str, Any]:
        """
        抽取三牌阵
        :param positions: 指定的牌位位置列表，如果为None则随机抽取
        :return: 包含三张牌和牌阵含义的完整结果
        """
        # 重新洗牌确保随机性
        self.shuffle_deck()
        
        cards = []
        
        if positions and len(positions) == 3:
            # 按指定位置抽牌
            for i, pos in enumerate(positions):
                if pos < 1 or pos > 78:
                    raise ValueError(f"牌位置必须在1-78之间，收到：{pos}")
                
                # 获取指定位置的牌（位置从1开始，数组从0开始）
                card = self.shuffled_deck[pos - 1]
                
                # 随机决定正逆位
                is_reversed = random.choice([True, False])
                
                # 构建抽牌结果
                drawn_card = {
                    **card,
                    "is_reversed": is_reversed,
                    "orientation": "逆位" if is_reversed else "正位",
                    "meaning": card["reversed_meaning"] if is_reversed else card["upright_meaning"],
                    "draw_order": i + 1,
                    "selected_position": pos
                }
                
                position_info = THREE_CARD_SPREAD_POSITIONS[i]
                drawn_card["position"] = position_info["position"]
                drawn_card["position_meaning"] = position_info["meaning"]
                drawn_card["position_description"] = position_info["description"]
                
                cards.append(drawn_card)
                self.drawn_cards.append(drawn_card)
            
            spread_description = f"根据你选择的数字位置({positions[0]}, {positions[1]}, {positions[2]})进行的三牌阵占卜"
        else:
            # 随机抽牌（原有逻辑）
            for i in range(3):
                card = self.draw_single_card()
                position_info = THREE_CARD_SPREAD_POSITIONS[i]
                
                # 添加牌位信息
                card["position"] = position_info["position"]
                card["position_meaning"] = position_info["meaning"]
                card["position_description"] = position_info["description"]
                
                cards.append(card)
            
            spread_description = "经典的过去-现在-未来牌阵，适合了解事件的发展脉络"
        
        return {
            "spread_type": "三牌阵",
            "spread_description": spread_description,
            "cards": cards,
            "total_cards": len(cards),
            "timestamp": random.randint(1000000, 9999999),
            "draw_method": "位置选择" if positions else "随机抽取"
        }
    
    def draw_custom_spread(self, num_cards: int, spread_name: str = "自定义牌阵") -> Dict[str, Any]:
        """
        抽取自定义数量的牌
        :param num_cards: 抽牌数量
        :param spread_name: 牌阵名称
        :return: 抽牌结果
        """
        if num_cards <= 0 or num_cards > 78:
            raise ValueError("抽牌数量必须在1-78之间")
        
        # 重新洗牌
        self.shuffle_deck()
        
        cards = []
        for i in range(num_cards):
            card = self.draw_single_card()
            card["position"] = i + 1
            card["position_meaning"] = f"第{i + 1}张牌"
            card["position_description"] = f"牌阵中的第{i + 1}个位置"
            cards.append(card)
        
        return {
            "spread_type": spread_name,
            "spread_description": f"包含{num_cards}张牌的自定义牌阵",
            "cards": cards,
            "total_cards": len(cards),
            "timestamp": random.randint(1000000, 9999999)
        }
    
    def get_deck_statistics(self) -> Dict[str, Any]:
        """获取牌库统计信息"""
        return {
            "total_cards": len(FULL_TAROT_DECK),
            "major_arcana": len([c for c in FULL_TAROT_DECK if c["arcana"] == "Major Arcana"]),
            "minor_arcana": len([c for c in FULL_TAROT_DECK if c["arcana"] == "Minor Arcana"]),
            "suits": {
                "Wands": len([c for c in FULL_TAROT_DECK if c.get("suit") == "Wands"]),
                "Cups": len([c for c in FULL_TAROT_DECK if c.get("suit") == "Cups"]),
                "Swords": len([c for c in FULL_TAROT_DECK if c.get("suit") == "Swords"]),
                "Pentacles": len([c for c in FULL_TAROT_DECK if c.get("suit") == "Pentacles"])
            },
            "drawn_cards": len(self.drawn_cards),
            "remaining_cards": len(FULL_TAROT_DECK) - len(self.drawn_cards)
        }


def format_card_for_ai(card: Dict[str, Any]) -> str:
    """
    格式化单张牌的信息供AI解读
    """
    orientation = "逆位" if card["is_reversed"] else "正位"
    
    result = f"""
【{card['name_zh']} ({card['name']})】- {orientation}
- 阿卡纳类型：{card['arcana']}
"""
    
    if card.get('suit'):
        result += f"- 花色：{card['suit']}"
        if card.get('element'):
            result += f"（{card['element']}元素）"
        result += "\n"
    
    result += f"""- 牌位含义：{card.get('position_meaning', '未知位置')}
- 当前含义：{card['meaning']}
- 牌面描述：{card['description']}
"""
    
    return result


def format_spread_for_ai(spread_result: Dict[str, Any]) -> str:
    """
    格式化整个牌阵的信息供AI解读
    """
    result = f"""
=== {spread_result['spread_type']} ===
{spread_result['spread_description']}

抽牌结果：
"""
    
    for i, card in enumerate(spread_result['cards'], 1):
        result += f"\n第{i}牌位：{card.get('position_meaning', f'第{i}位置')}"
        result += f"\n{card.get('position_description', '')}"
        result += format_card_for_ai(card)
        result += "\n" + "="*50 + "\n"
    
    result += f"""
本次抽牌总结：
- 牌阵类型：{spread_result['spread_type']}
- 抽牌张数：{spread_result['total_cards']}张
- 抽牌时间戳：{spread_result['timestamp']}
"""
    
    return result


# 创建全局实例
tarot_drawer = TarotCardDrawer()


def draw_tarot_reading(question: str = "", spread_type: str = "three_card", 
                      draw_mode: str = "random", positions: Optional[List[int]] = None) -> tuple[str, Dict[str, Any]]:
    """
    执行塔罗抽牌并返回格式化结果
    :param question: 用户问题
    :param spread_type: 牌阵类型 ("three_card", "single", "custom")
    :param draw_mode: 抽牌模式 ("random", "numbers")
    :param positions: 指定的牌位位置列表（当draw_mode为"numbers"时使用）
    :return: (格式化的抽牌结果字符串, 原始抽牌数据)
    """
    if spread_type == "single":
        # 单牌抽取
        card = tarot_drawer.draw_single_card()
        spread_result = {
            "spread_type": "单牌占卜",
            "spread_description": "抽取一张牌来回答你的问题",
            "cards": [card],
            "total_cards": 1,
            "timestamp": random.randint(1000000, 9999999)
        }
    elif spread_type == "three_card":
        # 三牌阵
        if draw_mode == "numbers" and positions and len(positions) == 3:
            spread_result = tarot_drawer.draw_three_card_spread(positions)
        else:
            spread_result = tarot_drawer.draw_three_card_spread()
    else:
        # 默认使用三牌阵
        spread_result = tarot_drawer.draw_three_card_spread()
    
    # 格式化结果
    formatted_result = format_spread_for_ai(spread_result)
    
    # 如果有问题，添加到开头
    if question.strip():
        formatted_result = f"您的问题：{question}\n\n{formatted_result}"
    
    return formatted_result, spread_result