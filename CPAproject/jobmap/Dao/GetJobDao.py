from common import MysqlCommon
from common.ResponseCommon import success, error
def get() -> dict:
    # 连接数据库
    conn = MysqlCommon.get_mysql_conn()
    # 创建游标对象
    cur = conn.cursor()
    try:
        # 查询命令
        sql = "SELECT * FROM job_profile"
        # 执行查询
        cur.execute(sql)
        # 得到查询结果
        result = cur.fetchall()
        return success(msg="提取成功", data=result)
    except Exception as e:
        return error(f"提取失败:{e}")
    finally:
        # 关闭连接
        MysqlCommon.close_mysql_conn(cur, conn)

#查询岗位名称做下拉列表
def query() -> dict:
    # 连接数据库
    conn = MysqlCommon.get_mysql_conn()
    # 创建游标对象
    cur = conn.cursor()
    try:
        # 查询命令
        sql = "SELECT job_name FROM job_profile"
        # 执行查询
        cur.execute(sql)
        # 得到查询结果
        result = cur.fetchall()
        return success(msg="提取成功", data=result)
    except Exception as e:
        return error(f"提取失败:{e}")
    finally:
        # 关闭连接
        MysqlCommon.close_mysql_conn(cur, conn)
if __name__ == '__main__':
    # res = get()
    # for res in res["data"]:
    #     res["skills"]=json.loads(res["skills"])
    #     res["certificates"]=json.loads(res["certificates"])
    #     print(res)
    res = query()
    li = []
    for res in res["data"]:
        res = res["job_name"]
        li.append(res)
    print(li)