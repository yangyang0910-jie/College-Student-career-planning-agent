from typing import TypedDict

class CareerState(TypedDict):
    user_id: int              # 用户ID
    target_position: str      # 目标岗位（从user_info.job_direction提取）
    user_info: dict           # 基础信息
    student_info: dict        # 学生能力画像（skills已是list）
    job_info: dict            # 岗位画像（skills已是list）
    paths: dict               # 图谱晋升/换岗路径
    match_result: dict        # 匹配结果
    rag_context: str          # RAG检索结果
    report: str               # 最终报告Markdown
    market_stats: dict        # 企业岗位数据集统计