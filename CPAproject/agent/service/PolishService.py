from prompt.builder_prompt import BuilderPromptYaml
from agent.dao.CareerPlanDao import get_report, save_report
from common.ModelCommon import LLM
import re

def get_model():
    model = None
    if model is None:
        model=LLM.load_model()
    return model
#ai润色
def polish_report(user_id: int, report_id: int) -> dict:
    result = get_report(report_id, user_id)
    if result.get("code") != 200 or not result.get("data"):
        return {"code": 404, "msg": "报告不存在"}
    content = result["data"].get("content") or ""
    target_job = result["data"].get("target_job") or ""
    if not content:
        return {"code": 400, "msg": "报告内容为空"}
    prompt = BuilderPromptYaml.get_prompt("polish.yaml").replace(
        "{report}", content)
    try:
        resp = get_model().invoke(prompt)
    except Exception as e:
        print(f"润色LLM调用失败: {e}")
        return {"code": 500, "msg": "润色失败，请稍后重试"}

    polished = (resp.content or "").strip()
    if not polished:
        return {"code": 500, "msg": "润色结果为空"}

    #比较润色前后报告中的数字是否被改变
    origin_nums = re.findall(r"\d+\.?\d*", content)
    new_nums = re.findall(r"\d+\.?\d*", polished)
    if len(origin_nums) != len(new_nums):
        return {"code": 500, "msg": "润色结果校验未通过，已保留原报告"}
    save_report(user_id, target_job, polished)
    return {"code": 200, "msg": "润色成功", "data": {"report": polished}}
