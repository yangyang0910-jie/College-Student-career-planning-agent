import json
from common.ResponseCommon import error,success
from jobmap.Dao.GetJobDao import get, query
from jobmap.Dao.GetNoeDao import get_jobmap
from jobmap.Dao.SaveNeoDao import save

#从mysql提取生成并保存
def get_profile() ->dict:
    data = get()
    if data["code"] != 200 or not data["data"]:
        return error(msg="提取失败")
    for res in data["data"]:
        res["skills"] = json.loads(res["skills"])
        res["certificates"] = json.loads(res["certificates"])
    return data

#存入neo4j
def save_noe() -> dict:
    profile = get_profile()
    data = save(profile)
    if data["code"] != 200:
        return error(data["msg"])
    return success(msg="存入失败")

#查询neo4j具体的图谱信息
def get_noe(job_name:str)->dict:
    data = get_jobmap(job_name)
    return success(data)

#用于前端展示列表
def get_job_name()->dict:
    data = query()
    li = []
    try:
        for res in data["data"]:
            res = res["job_name"]
            li.append(res)
        return success(data=li)
    except Exception as e:
        return error("查询失败")



if __name__ == '__main__':
    res= get_noe("Java")
    print(res)