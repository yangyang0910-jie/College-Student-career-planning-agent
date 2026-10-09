from common.Noe4jCommon import get_neo4j_conn
from common.ResponseCommon import error,success
from jobmap.util.RelationUtil import PROMOTE, SWITCH

def save(profile:dict)->dict:
    graph = get_neo4j_conn()
    #创建岗位节点
    try:
        for item in profile["data"]:
            graph.query( """MERGE (j:Job {name: $name})
                   SET j.summary       = $summary,
                       j.education_req = $edu,
                       j.major_req     = $major,
                       j.salary_avg    = $salary,
                       j.innovation    = $innov,
                       j.learning      = $learn,
                       j.pressure      = $press,
                       j.communication = $comm,
                       j.internship    = $intern,
                       j.skills        = $skills,
                       j.certificates  = $certs""",
                         params={
                             "name": item["job_name"],
                             "summary": item.get("job_desc_summary"),
                             "edu": item.get("education_req"),
                             "major": item.get("major_req"),
                             "salary": item.get("salary_avg"),
                             "innov": item.get("innovation_score"),
                             "learn": item.get("learning_score"),
                             "press": item.get("pressure_score"),
                             "comm": item.get("communication_score"),
                             "intern": item.get("internship_score"),
                             "skills": item.get("skills", []),
                             "certs": item.get("certificates", []),
                         },
                         )
            for sk in item["skills"]:
                if not sk:
                    continue
                graph.query(
                    """MERGE (s:Skill {name: $sk})
                       WITH s 
                       MATCH (j:Job {name: $job})
                       MERGE (j)-[:要求]->(s)
                    """,
                    params={"sk": sk, "job": item["job_name"]},
                )
            for a, b in PROMOTE:
                graph.query(
                    """
                    MATCH (a:Job {name:$a}), (b:Job {name:$b})
                    MERGE (a)-[:晋升]->(b)
                    """,
                    params={"a": a, "b": b},
                )
            for a, b in SWITCH:
                graph.query(
                    """MATCH (a:Job {name:$a}), (b:Job {name:$b})
                       MERGE (a)-[:换岗]->(b)""",params = {"a": a, "b": b})
            print("节点:", graph.query(
                "MATCH (n) RETURN labels(n)[0] AS label, count(*) AS cnt"))
            print("关系:", graph.query(
                "MATCH ()-[r]->() RETURN type(r) AS t, count(*) AS c"))
        return success("存入成功")
    except Exception as e:
        return error(msg="存入失败")