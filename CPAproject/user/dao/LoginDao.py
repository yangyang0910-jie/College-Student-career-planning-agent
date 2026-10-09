from  common import MysqlCommon
from common.ResponseCommon import error,success

def verify(email:str) -> dict:
    # 连接数据库
    conn = MysqlCommon.get_mysql_conn()
    # 创建游标对象
    cur = conn.cursor()
    try:
        # 查询命令
        sql = "SELECT * FROM users WHERE email = %s "
        # 执行查询
        cur.execute(sql,[email])
        # 得到查询结果
        result = cur.fetchall()
        print(f"查询结果：{result}")
        # 判断用户是否存在
        # 没查到用户时返回的是空元组
        if result:
            return success(result[0])
        return error("用户不存在")
    except Exception as e:
        return error(f"查询失败:{e}")
    finally:
        # 关闭连接
        MysqlCommon.close_mysql_conn(cur, conn)
if __name__ == '__main__':
    r = verify("3")
    print(r)
