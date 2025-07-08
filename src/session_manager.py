import uuid
import time
from typing import Dict, List, Optional, Any
from src.models import DivinationSession, ChatMessage


class SessionManager:
    """会话管理器 - 管理占卜追问的会话状态"""
    
    def __init__(self):
        self.sessions: Dict[str, DivinationSession] = {}
    
    def create_session(self, original_divination: Dict[str, Any]) -> str:
        """创建新的占卜会话"""
        session_id = str(uuid.uuid4())
        session = DivinationSession(
            session_id=session_id,
            original_divination=original_divination,
            messages=[],
            follow_up_count=0,
            created_at=time.time()
        )
        self.sessions[session_id] = session
        return session_id
    
    def get_session(self, session_id: str) -> Optional[DivinationSession]:
        """获取会话"""
        return self.sessions.get(session_id)
    
    def add_message(self, session_id: str, role: str, content: str) -> bool:
        """添加消息到会话"""
        session = self.get_session(session_id)
        if not session:
            return False
        
        message = ChatMessage(
            role=role,
            content=content,
            timestamp=time.time()
        )
        
        session.messages.append(message)
        
        # 保持最近5条消息的上下文
        if len(session.messages) > session.max_context_messages:
            session.messages = session.messages[-session.max_context_messages:]
        
        return True
    
    def increment_follow_up(self, session_id: str) -> bool:
        """增加追问次数"""
        session = self.get_session(session_id)
        if not session:
            return False
        
        session.follow_up_count += 1
        return True
    
    def can_follow_up(self, session_id: str) -> bool:
        """检查是否还能继续追问"""
        session = self.get_session(session_id)
        if not session:
            return False
        
        return session.follow_up_count < session.max_follow_ups
    
    def get_context_messages(self, session_id: str) -> List[Dict[str, str]]:
        """获取上下文消息（用于AI调用）"""
        session = self.get_session(session_id)
        if not session:
            return []
        
        # 转换为OpenAI API格式
        messages = []
        for msg in session.messages:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        return messages
    
    def get_original_divination_summary(self, session_id: str) -> str:
        """获取原始占卜的简要信息"""
        session = self.get_session(session_id)
        if not session:
            return ""
        
        original = session.original_divination
        if original.get("prompt_type") == "plum_flower":
            plum_flower = original.get("plum_flower", {})
            number = plum_flower.get("number", "")
            use_custom_time = plum_flower.get("use_custom_time", False)
            custom_datetime = plum_flower.get("custom_datetime", "")
            question = original.get("prompt", "")
            
            time_info = f"（自定义时间：{custom_datetime}）" if use_custom_time else "（当前时间）"
            return f"原始梅花易数占卜：数字{number}{time_info}，问题：{question}"
        else:
            return f"原始{original.get('prompt_type', '')}占卜：{original.get('prompt', '')}"
    
    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """清理超过指定时间的会话"""
        current_time = time.time()
        cutoff_time = current_time - (max_age_hours * 3600)
        
        to_remove = []
        for session_id, session in self.sessions.items():
            if session.messages:
                # 有消息的会话，检查最后消息时间
                last_message_time = session.messages[-1].timestamp
                if last_message_time < cutoff_time:
                    to_remove.append(session_id)
            else:
                # 没有消息的会话，检查创建时间
                if session.created_at > 0 and session.created_at < cutoff_time:
                    to_remove.append(session_id)
        
        for session_id in to_remove:
            del self.sessions[session_id]
        
        return len(to_remove)  # 返回清理的会话数量


# 全局会话管理器实例
session_manager = SessionManager()