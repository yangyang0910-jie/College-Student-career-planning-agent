#
import pandas as pd
from common import MysqlCommon
#读取文件
path = r"D:\workspace\CPAproject\岗位数据.xls"
df = pd.read_excel(path)
# 第一次去重：完全相同的记录去重
df = df.drop_duplicates()
print("完全去重后：", len(df))

# 第二次去重：岗位名称 + 岗位详情的内容相同的数据去重
df = df.drop_duplicates(subset=["岗位名称", "岗位详情"])

# 去掉岗位详情为空的数据：用于后面的岗位画像分析
profile_df = df.dropna(subset=["岗位详情"]).copy()

raw_df = df
# 名字映射---把中文表面改为英文
clean_df = raw_df.rename(columns={
    "岗位名称": "job_name",
    "地址": "work_city",
    "薪资范围": "salary",
    "公司名称": "company_name",
    "所属行业": "industry",
    "公司规模": "company_size",
    "公司类型": "company_type",
    "岗位编码": "job_code",
    "岗位详情": "job_desc",
    "公司详情": "company_desc",
})

# 要导入数据库的字段
COLS = [
    "job_name",
    "work_city",
    "salary",
    "company_name",
    "industry",
    "company_size",
    "company_type",
    "job_code",
    "job_desc",
    "company_desc"
]
# 只保留需要的字段
clean_df = clean_df[COLS]
# 岗位名称不能为空
clean_df = clean_df.dropna(subset=["job_name"])
print("准备导入数据库的数据：", len(clean_df))


conn = MysqlCommon.get_mysql_conn()
cur = conn.cursor()
cur.execute("TRUNCATE TABLE job_position")
sql = """
INSERT INTO job_position
(   job_name,
    work_city,
    salary,
    company_name,
    industry,
    company_size,
    company_type,
    job_code,
    job_desc,
    company_desc
)
VALUES
(%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)
"""
success = 0
fail = 0
# 一行一行地存进数据库，存之前清洗数据
for _, row in clean_df.iterrows():
    values = []
    for col in COLS:
        # 从当前行中取出当前字段
        value = row[col]
        if pd.isna(value):
            values.append(None)
        elif col == "job_desc":
            values.append(str(value).strip()[:8000])
        elif col == "company_desc":
            values.append(str(value).strip()[:4000])
        else:
            values.append(str(value).strip()[:200])
    try:
        # 把当前这一行插入 MySQL
        cur.execute(sql, values)
        success += 1
    except Exception as e:
        fail += 1
        if fail <= 3:
            print("失败样例：", e)
conn.commit()
MysqlCommon.close_mysql_conn(cur, conn)
print("岗位数据导入完成")
print("成功插入：", success)
print("失败数量：", fail)