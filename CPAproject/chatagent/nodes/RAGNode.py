from chatagent.state.ChatState import ChatState
from chatagent.tool.QueryTool import career_rag_search
def knowledge_node(state: ChatState) -> dict:
    data = career_rag_search.invoke({"question": state["question"]})
    if "没有检索到" in data or "不可用" in data:
        # 通用文档再试一次
        data += "\n\n（补充检索）\n" + career_rag_search.invoke({"question": "就业形势 应届生 求职"})
    print(f"[RAG] 命中 {len(data)} 字符")
    return {"rag_context": data}