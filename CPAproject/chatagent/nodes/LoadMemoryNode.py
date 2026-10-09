from chatagent.state.ChatState import ChatState
from chatagent.memory.SimpleMemory import SimpleMemory

def load_memory_node(state: ChatState) -> dict:
    memory = SimpleMemory(state["user_id"], state["session_id"])
    result = memory.build_memory_context(state["question"])
    if result:
        print(f"[四层记忆] 已加载 {len(result)} 字符")
    return {"memory_context": result}