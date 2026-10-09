from typing import Any
import json
# 四维度权重
WEIGHTS = {"基础要求": 0.15,"职业技能": 0.35,"职业素养": 0.30,"发展潜力": 0.20}

# 技能列表归一化：统一小写、去空格、返回集合
def norm_skills(skills: Any) -> set[str]:
    if not skills:
        return set()
    # 转JSON
    if isinstance(skills, str):
        try:
            skills = json.loads(skills)
        except json.JSONDecodeError:
            skills = [skills]
    # 转列表
    if not isinstance(skills, (list, tuple, set)):
        skills = [skills]
    # 小写、去空格
    result = set()
    for x in skills:
        if x is None:
            continue
        s = str(x).strip().lower()
        if s:
            result.add(s)
    return result
# 学历 + 专业判断
#基础要求判定:学历达标、专业相关
def edu_ok(student: dict, job: dict) -> bool:

    edu_rank = {"大专": 1,"本科": 2,"硕士": 3,"博士": 4}
    # 学生学历
    student_education = (student.get("education") or "").strip()
    # 找不到学历就默认本科
    student_rank = edu_rank.get(student_education,2)
    # 岗位学历要求
    job_education_req = (job.get("education_req") or "").strip()
    # 没有学历要求
    if not job_education_req:
        req_min = 1
    else:
        found_ranks = []
        for education, rank in edu_rank.items():
            if education in job_education_req:
                found_ranks.append(rank)
        # 找不到明确学历时，默认大专
        req_min = max(found_ranks,default=1)
    # 学历基础要求不满足返回False
    if student_rank < req_min:
        return False

    # 专业判断
    major = (student.get("major") or "").strip()
    # 取岗位专业要求
    req_major = (job.get("major_req") or "").strip()
    # 岗位没有专业要求
    if not req_major:
        return True
    # 岗位写专业不限
    if "不限" in req_major:
        return True
    # 学生没有填写专业
    if not major:
        return False
    # 完整包含
    if major in req_major or req_major in major:
        return True
    # 简单关键词匹配----模糊匹配
    keywords = [
        "计算机",
        "软件工程",
        "信息工程",
        "信息管理",
        "人工智能",
        "网络工程",
        "数据科学",
        "电子信息",
    ]
    for keyword in keywords:
        if keyword in major and keyword in req_major:
            return True
    return False
# 单项能力匹配
def gap_score(student_score: int, job_score: int) -> int:
    #根据学生能力和岗位要求计算匹配分：每低1分扣2分，学生超过岗位要求：不额外加分
    student_score = max(0,min(100, int(student_score)))
    job_score = max(0,min(100, int(job_score)))
    gap = max(0,job_score - student_score)
    return max(0,100 - gap * 2)
# 评价
def comment(total: float, gaps: list) -> str:
    #根据综合匹配度生成可解释结论。
    if total >= 85:
        tail = ("整体匹配度高，可针对性准备面试冲刺。")
    elif total >= 70:
        tail = ("整体匹配度良好，补齐关键技能缺口后竞争力将进一步提升。")
    elif total >= 55:
        tail = ("具备一定基础，需系统补强核心技能后再冲刺该岗位。")
    else:
        tail = ("与该岗位存在一定差距，建议先夯实基础或考虑相近的转型岗位。")
    if gaps:
        tail += (f"当前最需补齐的技能：{'、'.join(gaps[:5])}。"
        )
    return tail
# 人岗匹配
def calc_match(student: dict,job: dict) -> dict:
    # 基础要求
    base_score = (100 if edu_ok(student, job) else 60)
    # 职业技能
    student_skills = (student.get("skills") or [])
    job_skills = (job.get("skills") or [])
    student_skill_set = norm_skills(student_skills)
    job_skill_set = norm_skills(job_skills)
    # 技能交集
    hit = (student_skill_set & job_skill_set)
    # 技能匹配度：技能匹配度 = 命中技能数 / 岗位要求技能数 × 100
    skill_score = int(len(hit) / max(1, len(job_skill_set))*100)
    # 技能缺口：学生没有的技能
    skill_gaps = []
    for skill in job_skills:
        if not isinstance(skill, str):
            continue
        normalized = (skill.strip().lower())
        if (normalized not in student_skill_set):
            skill_gaps.append(normalized)

    # 职业素养
    # 学习能力匹配分
    learning_score = gap_score(
        student.get("learning_score") or 50,
        job.get("learning_score") or 60,
    )
    # 抗压能力匹配分
    pressure_score = gap_score(
        student.get("pressure_score") or 50,
        job.get("pressure_score") or 60,
    )
    # 沟通能力匹配分
    communication_score = gap_score(
        student.get("communication_score") or 50,
        job.get("communication_score") or 60,
    )
    quality = round((learning_score+pressure_score+communication_score)/3)

    # 发展潜力
    innovation_score = gap_score(
        student.get("innovation_score") or 50,
        job.get("innovation_score") or 60,
    )
    internship_score = gap_score(
        student.get("internship_score") or 50,
        job.get("internship_score") or 60,
    )
    # 证书
    certificates = (student.get("certificates") or [])
    if isinstance(certificates, str):
        try:
            certificates = json.loads(certificates)
        except json.JSONDecodeError:
            certificates = [certificates]
    cert_bonus = min(100,len(certificates) * 20)
    potential = round(innovation_score * 0.4+internship_score * 0.4+cert_bonus * 0.2)
    # 四维度
    dimensions = {
        "基础要求": base_score,
        "职业技能": skill_score,
        "职业素养": quality,
        "发展潜力": potential,
    }

    # 综合匹配度
    total = round(sum(dimensions[key] * WEIGHTS[key] for key in WEIGHTS),1)
    return {
        # 综合匹配度
        "total": total,
        # 四维度
        "dimensions": dimensions,
        # 权重
        "weights": WEIGHTS,
        # 前端能力对比
        "detail": {
            "innovation": {
                "student": student.get("innovation_score") or 50,
                "job": job.get("innovation_score") or 60,
            },
            "learning": {
                "student": student.get("learning_score") or 50,
                "job": job.get("learning_score") or 60,
            },
            "pressure": {
                "student": student.get("pressure_score") or 50,
                "job": job.get("pressure_score") or 60,
            },
            "communication": {
                "student": student.get("communication_score") or 50,
                "job": job.get("communication_score") or 60,
            },
            "internship": {
                "student": student.get("internship_score") or 50,
                "job": job.get("internship_score") or 60,
            },
        },
        # 技能匹配
        "skill_hit": sorted(hit),
        "skill_gaps": skill_gaps,
        # AI 可直接使用的评价
        "comment": comment(
            total,
            skill_gaps
        ),
    }

# 测试
if __name__ == "__main__":
    student = {
        "education": "本科",
        "major": "软件工程",
        "skills": [
            "Java",
            "Python",
            "MySQL",
            "Spring Boot",
            "Git",
        ],
        "certificates": [
            "英语四级",
            "计算机二级",
        ],
        "innovation_score": 50,
        "learning_score": 70,
        "communication_score": 80,
        "pressure_score": 50,
        "internship_score": 70,
    }
    job = {
        "education_req": "本科及以上",
        "major_req": (
            "计算机、软件工程及相关专业"
        ),
        "skills": [
            "Java",
            "Spring Boot",
            "MyBatis",
            "MySQL",
            "Redis",
            "MQ",
            "Linux",
            "Git",
            "分布式",
            "JVM调优",
        ],
        "innovation_score": 70,
        "learning_score": 80,
        "communication_score": 75,
        "pressure_score": 70,
        "internship_score": 55,
    }
    print(
        json.dumps(calc_match(student,job),ensure_ascii=False,indent=2)
    )