from common import MysqlCommon
from common.ResponseCommon import success

#查询出存入的所有岗位数据集
def query_jobprofile(job_name: str) -> dict:
    # 连接数据库
    conn = MysqlCommon.get_mysql_conn()
    # 创建游标对象
    cur = conn.cursor()
    try:
        # 查询命令
        sql = "SELECT job_desc FROM job_position WHERE job_name=%s AND job_desc IS NOT NULL LIMIT 30"
        # 执行查询
        cur.execute(sql, [job_name])
        # 得到查询结果
        result = cur.fetchall()
        print(f"数据库查出{result}")
        return success(result)
    except Exception as e:
        print(e)
    finally:
        MysqlCommon.close_mysql_conn(cur, conn)
if __name__ == '__main__':
    re=query_jobprofile("JAVA")
    print(re)