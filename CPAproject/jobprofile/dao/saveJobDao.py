from common import MysqlCommon
from common.ResponseCommon import error, success

#存入职业画像
class SaveJobProfileDao:
    @staticmethod
    def save(job_name:str,profile:dict) -> dict:
        # 连接数据库
        conn = MysqlCommon.get_mysql_conn()
        # 创建游标对象
        cur = conn.cursor()
        try:
            # 插入命令
            sql = """INSERT INTO job_profile
                        (job_name, education_req, major_req, skills, certificates,
                         salary_avg, innovation_score, learning_score,
                         pressure_score, communication_score, internship_score,
                         job_desc_summary)
                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                     ON DUPLICATE KEY UPDATE
                        job_name=VALUES(job_name), 
                        education_req=VALUES(education_req),
                        major_req=VALUES(major_req), 
                        skills=VALUES(skills),
                        certificates=VALUES(certificates),
                        salary_avg=VALUES(salary_avg),
                        innovation_score=VALUES(innovation_score), 
                        learning_score=VALUES(learning_score),
                        pressure_score=VALUES(pressure_score),
                        communication_score=VALUES(communication_score),
                        internship_score=VALUES(internship_score),
                        job_desc_summary=VALUES(job_desc_summary)
                        """
            # 执行查询
            cur.execute(sql, [
                job_name,
                profile.get("education_req"),
                profile.get("major_req"),
                profile.get("skills"),
                profile.get("certificates"),
                profile.get("salary_avg"),
                profile.get("innovation_score"),
                profile.get("learning_score"),
                profile.get("pressure_score"),
                profile.get("communication_score"),
                profile.get("internship_score"),
                profile.get("job_desc_summary"),
                ])
            conn.commit()
            print("保存成功")
            return success(msg="保存成功")
        except Exception as e:
            conn.rollback()
            print(f"画像保存失败: {e}")
            return error("画像保存失败")
        finally:
            # 关闭连接
            MysqlCommon.close_mysql_conn(cur, conn)

    #查询职业画像是否存在
    @staticmethod
    def query(job_name:str)-> dict:
        # 连接数据库
        conn = MysqlCommon.get_mysql_conn()
        # 创建游标对象
        cur = conn.cursor()
        try:
            sql = "SELECT id FROM job_profile WHERE job_name = %s LIMIT 1"
            cur.execute(sql, (job_name))
            result = cur.fetchone()
            if result is None:
                return error("画像不存在")
            return success(msg="已有画像",data=result["id"])
        except Exception as e:
            print(f"查询岗位画像是否存在失败：{e}")
            return error("查询失败")
    #查询所有的岗位画像
    @staticmethod
    def query_all(job_name: str) -> dict:
        # 连接数据库
        conn = MysqlCommon.get_mysql_conn()
        # 创建游标对象
        cur = conn.cursor()
        try:
            sql = "SELECT * FROM job_profile WHERE job_name = %s LIMIT 1"
            cur.execute(sql, [job_name])
            result = cur.fetchone()
            return success(data=result)
        except Exception as e:
            print(f"查询岗位画像失败：{e}")
            return error("查询失败")




    @staticmethod
    def get_market_stats(job_name: str) -> dict:
        #从企业岗位数据集统计目标岗位的市场画像
        stats = {
            "岗位记录数": 0,
            "招聘城市Top3": [],
            "代表企业Top3": [],
            "所属行业Top3": [],
        }
        conn = MysqlCommon.get_mysql_conn()
        cur = conn.cursor()
        try:
            # 总记录数
            cur.execute(
                "SELECT COUNT(*) AS c FROM job_position WHERE job_name=%s",
                (job_name,))
            row = cur.fetchone()
            stats["岗位记录数"] = row["c"] if row else 0
            if stats["岗位记录数"] == 0:
                return stats  # 数据集里没这个岗位，返回默认值

            # 三个维度的 Top3（城市/企业/行业）
            for key, col in (("招聘城市Top3", "work_city"),
                             ("代表企业Top3", "company_name"),
                             ("所属行业Top3", "industry")):
                cur.execute(
                    f"SELECT {col} AS k, COUNT(*) AS c FROM job_position "
                    f"WHERE job_name=%s AND {col} IS NOT NULL AND {col} != '' "
                    f"GROUP BY {col} ORDER BY c DESC LIMIT 3",
                    (job_name,))
                stats[key] = [f"{r['k']}（{r['c']}条）" for r in cur.fetchall()]
            return stats
        except Exception as e:
            print(f"市场统计失败: {e}")
            return stats
        finally:
            MysqlCommon.close_mysql_conn(cur, conn)
if __name__ == '__main__':
    res=SaveJobProfileDao.query_all("JAVA")
    print(res)