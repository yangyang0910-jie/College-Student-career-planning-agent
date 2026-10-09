from common import MysqlCommon
from common.ResponseCommon import success, error
def save_report(user_id: int, target_job: str, content: str) -> dict:
    conn = MysqlCommon.get_mysql_conn()
    cur = conn.cursor()
    try:
        sql = "INSERT INTO career_plan (user_id, target_job, content) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE content = VALUES(content)"
        cur.execute(sql, (user_id, target_job, content))
        conn.commit()
        return success("报告已保存")
    except Exception as e:
        conn.rollback()
        print(f"报告保存失败: {e}")
        return error("报告保存失败")
    finally:
        MysqlCommon.close_mysql_conn(cur, conn)
def list_reports(user_id: int) -> dict:
    #历史报告列表
    conn = MysqlCommon.get_mysql_conn()
    cur = conn.cursor()
    try:
        sql="SELECT id, target_job, create_time, update_time FROM career_plan WHERE user_id=%s ORDER BY update_time DESC"
        cur.execute(sql, (user_id,))
        return success(data=cur.fetchall())
    except Exception as e:
        print(f"报告列表失败: {e}")
        return error("查询失败")
    finally:
        MysqlCommon.close_mysql_conn(cur, conn)

#提取报告
def get_report(report_id: int, user_id: int) -> dict:
    #按id取单份报告正文
    conn = MysqlCommon.get_mysql_conn()
    cur = conn.cursor()
    try:
        sql="SELECT content, target_job FROM career_plan WHERE id=%s AND user_id=%s"
        cur.execute(sql, (report_id, user_id))
        row = cur.fetchone()
        return success(data=row or {})
    finally:
        MysqlCommon.close_mysql_conn(cur, conn)
#删除报告
def delete_report(report_id: int, user_id: int) -> dict:
    conn = MysqlCommon.get_mysql_conn()
    cur = conn.cursor()
    try:
        sql = "DELETE FROM career_plan WHERE id=%s AND user_id=%s"
        cur.execute(sql, (report_id, user_id))
        conn.commit()
        if cur.rowcount == 0:
            return error("报告不存在")
        return success(msg="删除成功")
    except Exception as e:
        conn.rollback()
        print(f"删除失败: {e}")
        return error("删除失败")
    finally:
        MysqlCommon.close_mysql_conn(cur, conn)
if __name__ == '__main__':
    res=delete_report(5, 7)
    print(res)
