import json
import uuid
import chromadb
import redis
from chromadb.utils import embedding_functions
from common import MysqlCommon
from userprofile.service.BaseInfoService import InfoService
from userprofile.dao.ProfileDao import StudentProfileDao
import os
from dotenv import load_dotenv
load_dotenv()
class SimpleMemory:
    def __init__(self, user_id: int, session_id: str):
        self.user_id = user_id
        self.session_id = session_id
        self.r = redis.StrictRedis(host="localhost", port=6379,db=1, decode_responses=True)
        self.win_key = f"chat_win:{session_id}"
        self.total_key = f"chat_total:{session_id}"
        client = chromadb.PersistentClient(path="chroma_memory")
        ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=os.getenv("MEMORY_EMBEDDING_MODEL_PATH"))
        self.collection = client.get_or_create_collection("chat_long_memory", embedding_function=ef)
    # 窗口记忆
    def add_window(self, role: str, content: str) -> None:
        msg = json.dumps({"role": role, "content": content}, ensure_ascii=False)
        self.r.rpush(self.win_key, msg)
        self.r.ltrim(self.win_key, -8, -1)
        self.r.expire(self.win_key, 3600)
        self.r.incr(self.total_key)
        self.r.expire(self.total_key, 3600)

    def load_window(self) -> list:
        return [json.loads(x) for x in self.r.lrange(self.win_key, 0, -1)]

    # 摘要记忆
    def load_summary(self) -> str:
        conn = MysqlCommon.get_mysql_conn()
        cur = conn.cursor()
        try:
            sql="SELECT summary FROM chat_summary WHERE session_id=%s"
            cur.execute(sql,[self.session_id])
            row = cur.fetchone()
            return (row or {}).get("summary", "")
        finally:
            MysqlCommon.close_mysql_conn(cur, conn)

    def save_summary(self, summary: str) -> None:
        conn = MysqlCommon.get_mysql_conn()
        cur = conn.cursor()
        try:
            sql="INSERT INTO chat_summary (session_id, summary) VALUES (%s, %s) ON DUPLICATE KEY UPDATE summary=VALUES(summary)"
            cur.execute(sql,[self.session_id, summary])
            conn.commit()
        finally:
            MysqlCommon.close_mysql_conn(cur, conn)

    # 摘要进度：累计已摘要的消息条数
    def load_summarized_count(self) -> int:
        n = self.r.get(f"chat_sum_count:{self.session_id}")
        return int(n) if n else 0

    def save_summarized_count(self, count: int) -> None:
        self.r.set(f"chat_sum_count:{self.session_id}", count, ex=3600)

    def load_total_count(self) -> int:
        n = self.r.get(self.total_key)
        return int(n) if n else 0

    # 长期记忆
    def add_long(self, content: str) -> None:
        mid = f"{self.user_id}{uuid.uuid4().hex}"
        self.collection.add(ids=[mid], documents=[content],metadatas=[{"user_id": self.user_id}])

    def load_long(self, question: str, k: int = 3) -> list:
        rs = self.collection.query(query_texts=[question], n_results=k,where={"user_id": self.user_id})
        return rs["documents"][0] if rs["documents"] else []

    # 用户画像
    def load_profile(self) -> str:
        base = InfoService.get_info(self.user_id) or {}
        stu = StudentProfileDao.query(self.user_id)
        stu = (stu.get("data") or {}) if stu.get("code") == 200 else {}

        skills = stu.get("skills")
        if isinstance(skills, str):
            try:
                skills = json.loads(skills)
            except json.JSONDecodeError:
                skills = []

        lines = []
        if base.get("name"):
            lines.append(f"姓名：{base['name']}")
        if base.get("education"):
            lines.append(f"学历：{base['education']}")
        if base.get("major"):
            lines.append(f"专业：{base['major']}")
        if base.get("job_direction"):
            lines.append(f"求职方向：{base['job_direction']}")
        if skills:
            lines.append(f"技能：{'、'.join(skills[:8])}")
        return "\n".join(lines)

    # 组装
    def build_memory_context(self, question: str) -> str:
        blocks = []
        profile = self.load_profile()
        if profile:
            blocks.append(f"【用户画像】\n{profile}")
        longs = self.load_long(question)
        if longs:
            blocks.append("【长期记忆】\n" + "\n".join(f"- {m}" for m in longs))
        summary = self.load_summary()
        if summary:
            blocks.append(f"【历史摘要】\n{summary}")
        window = self.load_window()
        if window:
            blocks.append(f"【最近对话】\n{window}")
        return "\n\n".join(blocks)