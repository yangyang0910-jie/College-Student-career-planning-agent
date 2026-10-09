from agent.state.CareerState import CareerState
from agent.util.MatchUtil import calc_match

# 四维度人岗匹配
def match_node(state: CareerState) -> dict:
    # 获取学生画像和岗位画像
    student = dict(state.get("student_info") or {})
    job = state.get("job_info") or {}
    base = state.get("user_info") or {}
    if not student:
        raise ValueError("state中缺少student_info")
    if not job:
        raise ValueError("state中缺少job_info")
    student.setdefault("education", base.get("education"))
    student.setdefault("major", base.get("major"))
    # 计算匹配度
    match_result = calc_match(student, job)
    return {"match_result": match_result}