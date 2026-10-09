from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.errors import GraphRecursionError
from chatagent.state.ChatState import ChatState
from chatagent.nodes.LoadMemoryNode import load_memory_node
from chatagent.nodes.IntentNode import intent_node
from chatagent.nodes.RAGNode import knowledge_node
from chatagent.nodes.ChatNode import chat_direct_node
from chatagent.nodes.AnswerNode import answer_node

def build_chat_graph():
    graph = StateGraph(ChatState)
    graph.add_node("load_memory", load_memory_node)
    graph.add_node("intent", intent_node)
    graph.add_node("knowledge_node", knowledge_node)
    graph.add_node("chat_direct", chat_direct_node)
    graph.add_node("answer", answer_node)

    # 画边
    graph.add_edge(START, "load_memory")
    graph.add_edge("load_memory", "intent")
    graph.add_conditional_edges("intent", route_by_intent, ["knowledge_node", "chat_direct"])
    graph.add_edge("knowledge_node", "answer")
    graph.add_edge("chat_direct", END)
    graph.add_edge("answer", END)
    return graph.compile(checkpointer=MemorySaver())

#意图识别路由：knowledge走知识库问答
#chat_direct会带上记忆里的用户画像，能回答"我"相关的问题
def route_by_intent(state: ChatState) -> str:
    if state["intent"] == "knowledge":
        return "knowledge_node"
    return "chat_direct"

async def stream(question: str, user_id: int, session_id: str) -> dict:
    graph = build_chat_graph()
    config = {"configurable": {"thread_id": session_id}, "recursion_limit": 20}
    try:
        async for mode, chunk in graph.astream({"question": question, "user_id": user_id,"session_id": session_id},config, stream_mode=["messages"]):
            if mode == "messages":
                msg, meta = chunk
                if msg.content and msg.content.strip():
                    yield {"delta": msg.content}
    except GraphRecursionError:
        yield {"error": "对话处理超限"}
    except Exception as e:
        yield {"error": str(e)}
    yield {"done": True}

def draw():
    graph = build_chat_graph()
    data = graph.get_graph().draw_mermaid_png()
    with open("222.png", "wb") as f:
        f.write(data)

if __name__ == '__main__':
    draw()