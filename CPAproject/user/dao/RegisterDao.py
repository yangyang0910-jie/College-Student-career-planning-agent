from common import MysqlCommon
from common.ResponseCommon import error,success

# 查询用户是否已经注册过
def query_user(email:str) -> dict:
    # 连接数据库
    conn = MysqlCommon.get_mysql_conn()
    # 创建游标对象
    cur = conn.cursor()
    try:
        # 查询命令
        sql = "SELECT * FROM users WHERE email = %s"
        # 执行查询
        cur.execute(sql,[email])
        # 得到查询结果
        result = cur.fetchall()
        # 判断用户是否存在
        if result:
            return error("用户已存在")
        return success("用户不存在")
    except Exception as e:
        return error(f"查询失败:{e}")
    finally:
        # 关闭连接
        MysqlCommon.close_mysql_conn(cur, conn)

# 将用户信息存入数据库
def save_user(username: str, email: str, hash_password: str) -> dict:
    # 连接数据库
    conn = MysqlCommon.get_mysql_conn()
    # 创建游标对象
    cur = conn.cursor()
    try:
        # 查询命令
        sql = "INSERT INTO `users` (id,username,email,password,create_time) VALUES (null,%s,%s,%s,NOW())"
        # 执行查询
        cur.execute(sql,[username, email, hash_password])
        #提交事务
        conn.commit()
        print("添加成功")
        return success(msg="添加成功")
        # 判断用户是否存在
    except Exception as e:
        return error(f"存入失败:{e}")
    finally:
        MysqlCommon.close_mysql_conn(cur, conn)

if __name__ == '__main__':
    r=save_user("测试3","333","444")
    print(r)
