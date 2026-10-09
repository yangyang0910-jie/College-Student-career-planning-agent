import json
from typing import Any
from agent.state.CareerState import CareerState
from common.ModelCommon import LLM
from prompt.builder_prompt import BuilderPromptYaml
from agent.dao.CareerPlanDao import save_report

model = LLM.load_model()
def to_json(obj: Any) -> str:
    #dict 转 JSON字符串
    return json.dumps(obj or {}, ensure_ascii=False, indent=2, default=str)
def build_prompt(state: dict, target_position: str) -> str:
    # 组装报告 Prompt
    parts = {
        "{target_position}": target_position,
        "{user_info}":    to_json(state.get("user_info")),
        "{student_info}": to_json(state.get("student_info")),
        "{job_info}":     to_json(state.get("job_info")),
        "{match_result}": to_json(state.get("match_result")),
        "{paths}":        to_json(state.get("paths")),
        "{rag_context}":  state.get("rag_context") or "",
        "{market_stats}": to_json(state.get("market_stats")),
    }
    for k, v in parts.items():
        if not isinstance(v, str):
            raise TypeError(f"Prompt注入值必须是str，检查to_json")
    prompt = BuilderPromptYaml.get_prompt("report_prompt.yaml")
    for placeholder, value in parts.items():
        prompt = prompt.replace(placeholder, value)
    return prompt

def get_report_node(state: CareerState) -> dict:
    #获取信息
    target_position = state.get("target_position")
    if not target_position:
        raise ValueError("state中缺少target_position，无法生成报告")
    prompt = build_prompt(state, target_position)
    full=[]
    try:
        for chunk in model.stream(prompt):
            piece = chunk.content or ""
            if piece:
                full.append(piece)
    except Exception as e:
        raise RuntimeError(f"报告生成LLM调用失败:{e}")

    report = "".join(full).strip()
    if not report:
        raise RuntimeError("报告生成为空，请重试")
    save_report(state["user_id"], target_position, report)
    print("保存成功")
    return {"report": report}