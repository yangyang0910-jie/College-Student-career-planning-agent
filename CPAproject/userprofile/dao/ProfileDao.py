import json
from common import MysqlCommon
from common.ResponseCommon import error, success
class StudentProfileDao:
    @staticmethod
    def save(user_id: int, raw_text: str, profile: dict,source:str)->dict:
        # 连接数据库
        conn = MysqlCommon.get_mysql_conn()
        # 创建游标对象
        cur = conn.cursor()
        try:
            # 插入命令
            sql = """INSERT INTO student_profile
                        (user_id, raw_text, skills, certificates, projects,
                         internships, competitions, strengths,
                         skill_score, innovation_score, learning_score,
                         communication_score, pressure_score, internship_score,
                         completeness, competitiveness, source)
                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                     ON DUPLICATE KEY UPDATE
                        raw_text=VALUES(raw_text), 
                        skills=VALUES(skills),
                        certificates=VALUES(certificates), 
                        projects=VALUES(projects),
                        internships=VALUES(internships),
                        competitions=VALUES(competitions),
                        strengths=VALUES(strengths), 
                        skill_score=VALUES(skill_score),
                        innovation_score=VALUES(innovation_score),
                        learning_score=VALUES(learning_score),
                        communication_score=VALUES(communication_score),
                        pressure_score=VALUES(pressure_score),
                        internship_score=VALUES(internship_score),
                        completeness=VALUES(completeness),
                        competitiveness=VALUES(competitiveness),
                        source=VALUES(source)"""
            # 执行查询
            cur.execute(sql, [
                            user_id,
                            raw_text,
                            profile["skills"],
                            profile["certificates"],
                            profile["projects"],
                            profile["internships"],
                            profile["competitions"],
                            profile["strengths"],
                            profile["skill_score"],
                            profile["innovation_score"],
                            profile["learning_score"],
                            profile["communication_score"],
                            profile["pressure_score"],
                            profile["internship_score"],
                            profile["completeness"],
                            profile["competitiveness"],
                            source,])
            conn.commit()
            return success(msg="画像生成成功")
        except Exception as e:
            conn.rollback()
            print(f"画像保存失败: {e}")
            return error("画像保存失败")
        finally:
            # 关闭连接
            MysqlCommon.close_mysql_conn(cur, conn)

    @staticmethod
    def query(user_id: int) -> dict:
        # 连接数据库
        conn = MysqlCommon.get_mysql_conn()
        # 创建游标对象
        cur = conn.cursor()
        try:
            # 查询命令
            sql = "SELECT * FROM student_profile WHERE user_id = %s"
            # 执行查询
            cur.execute(sql, [user_id])
            # 得到查询结果
            result = cur.fetchone()
            #转为json格式
            if result:
                for key in ("skills","certificates","projects","internships","competitions"):
                    result[key] = json.loads(result.get(key))
                print(f"转换之后：{result}")
                return success(result)
            else:
                return success(msg="暂时没有画像")
        except Exception as e:
            return error(f"查询失败:{e}")
        finally:
            # 关闭连接
            MysqlCommon.close_mysql_conn(cur, conn)
if __name__ == '__main__':
    res = StudentProfileDao.query(7)
    print(res)