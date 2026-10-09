from langchain_core.messages import HumanMessage
from chatagent.state.ChatState import ChatState
from chatagent.schema.IntentSchema import IntentSchema
from common.ModelCommon import LLM
from prompt.builder_prompt import BuilderPromptYaml
from langchain.agents import create_agent
model = LLM.load_model()

def intent_node(state: ChatState) -> dict:
    question = state["question"]
    try:
        intent_prompt = BuilderPromptYaml.get_prompt("intent.yaml").replace("{question}", question)
        intent_agent = create_agent(
            model=model,
            system_prompt=intent_prompt,
            response_format=IntentSchema,
        )
        rs = intent_agent.invoke({"messages": [HumanMessage(content=question)]})
        intent= rs["structured_response"].intent
    except Exception as e:
        # 意图识别失败时兜底为chat，保证对话不中断
        print(f"[意图识别] 失败，兜底为chat: {e}")
        intent = "chat"
    print(f"[意图识别] {state['question']} -> {intent}")
    return {"intent": intent}