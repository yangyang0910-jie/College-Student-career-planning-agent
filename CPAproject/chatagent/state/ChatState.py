from typing import TypedDict

class ChatState(TypedDict):
    user_id: int
    session_id: str
    question: str
    intent: str          # 识别knowledge / chat
    memory_context: str  # 四层记忆组装块
    rag_context: str     # knowledge：知识库检索结果
    answer: str          # 最终回答