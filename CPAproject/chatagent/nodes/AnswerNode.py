from chatagent.state.ChatState import ChatState
from common.ModelCommon import LLM
from prompt.builder_prompt import BuilderPromptYaml

# 单例：只加载一次
model = LLM.load_model()
answer_prompt = BuilderPromptYaml.get_prompt("RAGanswer.yaml")
def answer_node(state: ChatState) -> dict:
    memory = (state.get("memory_context") or "").strip()
    rag = (state.get("rag_context") or "").strip()
    question = (state.get("question") or "").strip()
    # 空问题兜底
    if not question:
        return {"answer": "请告诉我你想了解的问题。"}
    # 分段拼接，带标题，空段自动省略
    sections = [answer_prompt]
    if memory:
        sections.append(f"【已知信息】\n{memory}")
    sections.append(f"【知识库资料】\n{rag or '暂无'}")
    sections.append(f"【用户问题】\n{question}")
    prompt = "\n\n".join(sections)
    # 模型调用异常兜底，不中断图
    try:
        answer = model.invoke(prompt).content.strip()
    except Exception as e:
        print(f"[answer_node] 模型调用失败: {e}")
        return {"answer": "抱歉，暂时无法回答，请稍后再试。"}
    return {"answer": answer}