import json
from typing import Any
def profileprocessor(profile: dict) -> dict:
    # 大模型返回的分数超过100时
    def clamp(v: Any) -> int:
        try:
            return max(0, min(100, int(v)))
        except (TypeError, ValueError):
            return 50

    # 计算完整度
    integrity = [profile.get("skills", []),
                 profile.get("certificates", []),
                 profile.get("projects", []),
                 profile.get("internships", []),
                 profile.get("competitions", []),
                 profile.get("strengths"),[]]
    count = 0
    for i in integrity:
        if i:
            count = count + 1
    completeness = int((count / len(integrity)) * 100)

    # 把所有的字典格式转为json字符串----要存入数据库不能直接存入dict/list
    skills = json.dumps(profile.get("skills", []), ensure_ascii=False)
    certificates = json.dumps(profile.get("certificates", []), ensure_ascii=False)
    projects = json.dumps(profile.get("projects", []), ensure_ascii=False)
    internships = json.dumps(profile.get("internships", []), ensure_ascii=False)
    competitions = json.dumps(profile.get("competitions", []), ensure_ascii=False)

    # 计算竞争力
    competitiveness = (clamp(profile.get("innovation_score"))
                       +clamp(profile.get("learning_score"))
                       +clamp(profile.get("communication_score"))
                       +clamp(profile.get("pressure_score"))
                       +clamp(profile.get("internship_score"))
                       )//5
    #打包返回方便存入数据库中
    return {
        "skills": skills,
        "certificates": certificates,
        "projects": projects,
        "internships": internships,
        "competitions": competitions,
        "strengths": profile.get("strengths") or None,
        "skill_score": clamp(profile.get("skill_score")),
        "innovation_score": clamp(profile.get("innovation_score")),
        "learning_score": clamp(profile.get("learning_score")),
        "communication_score": clamp(profile.get("communication_score")),
        "pressure_score": clamp(profile.get("pressure_score")),
        "internship_score": clamp(profile.get("internship_score")),
        "competitiveness": competitiveness,
        "completeness": completeness,
    }