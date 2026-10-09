from common import Noe4jCommon
#查某岗位的晋升路径 + 换岗路径
def get_jobmap(job_name: str) -> dict:
    graph = Noe4jCommon.get_neo4j_conn()
    job_info = graph.query(
        "MATCH (n:Job {name:$n}) RETURN n",
        params={"n": job_name}
    )
    #查询晋升
    promote = graph.query(
        """MATCH p=(a:Job {name:$n})-[:晋升*1..3]->(b:Job)
        RETURN [x IN nodes(p) | x.name] AS path""",
        params={"n": job_name}
    )
    #查询换岗
    switch = graph.query(
        """MATCH (a:Job {name:$n})-[:换岗]->(b:Job)
           RETURN b.name AS name, b.summary AS summary""",
        params={"n": job_name})

    return {"job": job_info, "promote": promote, "switch": switch}
if __name__ == '__main__':
    res=get_jobmap("Java")
    print(res)