from agent.state.CareerState import CareerState
from agent.tools.RagTool import job_rag_search

# RAG检索：行业趋势+技能提升方向（按岗位+技能缺口构造查询）
def rag_node(state: CareerState) -> dict:
    # 获取信息
    job_info = state.get("job_info") or {}
    match_result = state.get("match_result") or {}
    job_name = job_info.get("job_name") or state.get("target_position") or ""
    missing_skills = match_result.get("skill_gaps", [])
    question = (
        f"{job_name} 岗位 行业发展趋势 社会需求 "
        f"技能提升方向 学习路线 {' '.join(missing_skills[:5])}"
    )
    try:
        #调用工具
        rag_context = job_rag_search.invoke({"question": question, "job_name": job_name})
    except Exception as e:
        raise RuntimeError(f"RAG检索异常:{e}")
    return {"rag_context": rag_context}
