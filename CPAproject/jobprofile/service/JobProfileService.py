import json
from common.ModelCommon import LLM
from common.ResponseCommon import error
from jobprofile.dao.QueryJobDao import query_jobprofile
from prompt.builder_prompt import BuilderPromptYaml
from jobprofile.dao.saveJobDao import SaveJobProfileDao

#提取生成并保存
def generate() -> None:
    # 20个就业岗位
    jobs =["Java",
           "C/C++",
           "前端开发",
           "软件测试",
           "测试工程师",
           "硬件测试",
           "质量管理/测试",
           "实施工程师",
           "技术支持工程师",
           "产品专员/助理",
           "项目经理/主管",
           "科研人员",
           "销售运营",
           "销售助理",
           "售后客服",
           "总助/CEO助理/董事长助理",
           "广告销售",
           "储备经理人",
           "储备干部",
           "管培生/储备干部",
           ]
    llm = LLM.load_model()
    for job_name in jobs:
        # 跳过已经生产的职业画像
        res = SaveJobProfileDao.query(job_name)
        if res["code"] == 200:
            print(f"跳过{res["data"]}")
            continue
        #查询所有岗位数据集
        job_desc = query_jobprofile(job_name)
        if job_desc["code"] != 200:
            print("查询失败")
            continue
        job_desc=job_desc["data"]
        des_list = []
        for index,row in enumerate(job_desc,start=1):
            desc = row.get("job_desc")
            if not desc:
                continue
            des_list.append(f"岗位{index}:{desc}")
        job_desc = "\n\n".join(des_list)
        job_desc = job_desc.replace("<br>", "\n")
        prompt = BuilderPromptYaml.get_prompt("job_profile.yaml").replace(
        "{job_desc}", job_desc)
        try:
            res = llm.invoke(prompt)
            print(f"大模型输出：{res.content}")
        except Exception as e:
            raise RuntimeError(f"岗位画像LLM调用失败：{e}") from e

        #兜底----大模型返回```json
        content = res.content.strip()
        if content.startswith("```"):
            content = content.replace("```json", "")
            content = content.replace("```", "")
            content = content.strip()
        try:
            data = json.loads(content)
            data["skills"]=json.dumps(data.get("skills"),ensure_ascii=False)
            data["certificates"] = json.dumps(data.get("certificates"), ensure_ascii=False)
            SaveJobProfileDao.save(job_name,data)
        except json.JSONDecodeError:
            print(f"{job_name} LLM返回的不是合法JSON")
            continue

#用于前端展示
def query_profile(job_name: str) -> dict :
    data = SaveJobProfileDao.query_all(job_name)
    if data.get("code") != 200 or not data.get("data"):
        return None
    row = data["data"]
    for key in ("skills", "certificates"):
        if isinstance(row.get(key), str):
            try:
                row[key] = json.loads(row[key])
            except json.JSONDecodeError:
                row[key] = []
    return row
if __name__ == '__main__':
    res=generate()
    print(res)