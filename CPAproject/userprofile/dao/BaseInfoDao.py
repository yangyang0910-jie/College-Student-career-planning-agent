import traceback
from typing import Any
from common import MysqlCommon
from common.ResponseCommon import error,success
from datetime import datetime
from userprofile.entity.BaseInfoEntity import SaveEntity
def _clean(v: Any) -> str | None:
    #None/空串/纯空格统一转为 None，保证库里'没填'都是NULL
    if v is None:
        return None
    v = str(v).strip()
    if v:
        return v
    else:
        return None
def _parse_date(time: str | None) -> str | None:
    # 把各种写法的时间格式转成 MySQL的DATE，转不了就返回 None
    cleaned = _clean(time)
    if cleaned is None:
        return None
    for item in ("%Y-%m-%d", "%Y-%m", "%Y.%m", "%Y/%m", "%Y年%m月", "%Y"):
        try:
            dt = datetime.strptime(cleaned,item)
            return dt.strftime("%Y-%m-%d")   # 2027-06-01 形式
        except ValueError:
            continue
    return None
# 保存用户基础信息
def info_save(saveinfoEntity: SaveEntity, user_id: int) -> dict:
    # 连接数据库
    conn = MysqlCommon.get_mysql_conn()
    # 创建游标对象
    cur = conn.cursor()
    try:
        # 日期先解析，解析失败给出友好提示
        parsed_date = _parse_date(saveinfoEntity.graduation_date)
        # 可能存在用户没填这个字段的情况，所以不能只判断传来的时间
        if saveinfoEntity.graduation_date and parsed_date is None:
            return error("毕业时间格式不正确，示例：2027-06 或 2027-06-30")
        # 查询命令----不存在就插入数据，存在就更新数据
        sql = """INSERT INTO user_profile 
                    (id,user_id,name,education, major, school,graduation_date, city, job_direction) 
                    VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON DUPLICATE KEY UPDATE
                        name=VALUES(name), 
                        education=VALUES(education),
                        major=VALUES(major), 
                        school=VALUES(school),
                        graduation_date=VALUES(graduation_date),
                        city=VALUES(city), 
                        job_direction=VALUES(job_direction)"""
        # 执行查询
        cur.execute(sql,[
            user_id,
            _clean(saveinfoEntity.name),
            _clean(saveinfoEntity.education),
            _clean(saveinfoEntity.major),
            _clean(saveinfoEntity.school),
            parsed_date,
            _clean(saveinfoEntity.city),
            _clean(saveinfoEntity.job_direction),])
        # 得到查询结果
        # 提交事务
        conn.commit()
        # 判断数据是否插入成功
        return success(msg="数据保存成功")
    except Exception as e:
        # 回滚事务
        conn.rollback()
        traceback.print_exc()
        # print(f"保存失败: {e}")
        return error("数据保存失败")
    finally:
        # 关闭连接
        MysqlCommon.close_mysql_conn(cur, conn)

def info_query(user_id:int)->dict:
    # 连接数据库
    conn = MysqlCommon.get_mysql_conn()
    # 创建游标对象
    cur = conn.cursor()
    try:
        # 查询命令
        sql = "SELECT * FROM user_profile WHERE user_id = %s "
        # 执行查询
        cur.execute(sql, [user_id])
        # 得到查询结果
        result = cur.fetchall()
        # print(result) #查出来的格式
        if result:
             return success(result[0])
        else:
            return error("用户信息不存在")
    except Exception as e:
        return error("查询失败")
    finally:
        # 关闭连接
        MysqlCommon.close_mysql_conn(cur, conn)

if __name__ == '__main__':
    re = info_query(6)
    print(re)
    # print(type(re["code"]))# int

