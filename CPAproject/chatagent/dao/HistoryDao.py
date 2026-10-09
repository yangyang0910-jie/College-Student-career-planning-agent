from common import MysqlCommon
from common.ResponseCommon import success,error

#保存历史记录
def save(session_id,user_id:int, question:str, answer:str)->dict:
    conn = MysqlCommon.get_mysql_conn()
    cur = conn.cursor()
    try:
        sql = "insert into chat_conversation(session_id,user_id,question,answer) values (%s, %s, %s, %s)"
        cur.execute(sql,[session_id,user_id,question,answer])
        conn.commit()
        return success(msg="保存成功")
    except Exception as e:
        conn.rollback()
        return error(msg=f"保存失败：{e}")
    finally:
        MysqlCommon.close_mysql_conn(cur,conn)

#查询历史记录列表
def history_list(user_id: int) -> list:
    conn = MysqlCommon.get_mysql_conn()
    cur = conn.cursor()
    try:
        sql = ("""SELECT c1.session_id,
                              MIN(c1.create_time) AS create_time,
                              (SELECT c2.question FROM chat_conversation c2
                               WHERE c2.session_id = c1.session_id
                               ORDER BY c2.id LIMIT 1) AS title
                       FROM chat_conversation c1
                       WHERE c1.user_id = %s
                       GROUP BY c1.session_id
                       ORDER BY create_time DESC""")
        cur.execute(sql,[user_id])
        return cur.fetchall()
    finally:
        MysqlCommon.close_mysql_conn(cur,conn)

#查询单个对话
def get_conversation(user_id: int, session_id: str) -> list:
    """单会话完整多轮对话（转成前端messages格式）"""
    conn = MysqlCommon.get_mysql_conn()
    cur = conn.cursor()
    try:
        cur.execute("""SELECT question, answer, create_time
                       FROM chat_conversation
                       WHERE user_id=%s AND session_id=%s ORDER BY id""",
                    (user_id, session_id))
        rows = cur.fetchall()
        msgs = []
        for r in rows:
            msgs.append({"role": "user", "content": r["question"]})
            msgs.append({"role": "assistant", "content": r["answer"]})
        return msgs
    finally:
        MysqlCommon.close_mysql_conn(cur, conn)
def delete_session(user_id: int, session_id: str) -> None:
    conn = MysqlCommon.get_mysql_conn()
    cur = conn.cursor()
    try:
        cur.execute("""DELETE FROM chat_conversation
                       WHERE user_id=%s AND session_id=%s""",
                    (user_id, session_id))
        conn.commit()
    finally:
        MysqlCommon.close_mysql_conn(cur, conn)