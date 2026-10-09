from chatagent.state.ChatState import ChatState
from common.ModelCommon import LLM
from prompt.builder_prompt import BuilderPromptYaml

model = LLM.load_model()
chat_prompt = BuilderPromptYaml.get_prompt("chat.yaml")

def chat_direct_node(state: ChatState) -> dict:
    #闲聊：结合记忆上下文，友好简短回应
    memory = (state.get("memory_context") or "").strip()
    question = (state.get("question") or "").strip()
    if not question:
        return {"answer": "你好，请问有什么可以帮你的？"}
    sections = [chat_prompt]
    if memory:
        sections.append(f"【已知信息】\n{memory}")
    sections.append(f"【用户问题】\n{question}")
    prompt = "\n\n".join(sections)
    try:
        answer = model.invoke(prompt).content.strip()
    except Exception as e:
        print(f"[chat_direct_node] 模型调用失败: {e}")
        return {"answer": "抱歉，我这边暂时有点问题，请稍后再试。"}
    return {"answer": answer}