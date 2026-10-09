#创建neo4j连接
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_neo4j import Neo4jGraph
#获取连接
def get_neo4j_conn() -> Neo4jGraph:
    return Neo4jGraph(
        url=os.getenv("NEO4J_URL"), #连接地址
        username=os.getenv("NEO4J_USERNAME"),#连接账号
        password=os.getenv("NEO4J_PASSWORD"),#连接密码
        database=os.getenv("NEO4J_DATABASE"),#数据库名称
    )