from agent.state.CareerState import CareerState
from userprofile.dao.ProfileDao import StudentProfileDao
import json

def load_student_node(state: CareerState) -> dict:
    user_id = state["user_id"]
    # 查询用户画像
    result = StudentProfileDao.query(user_id)
    if result.get("code") != 200 or not result.get("data"):
        raise ValueError("学生画像不存在，请先在画像页生成画像")
    data = result["data"]
    for key in ("skills", "certificates"):
        v = data.get(key)
        # 将这两个从数据库中取出的 转为列表
        if isinstance(v, str):
            try:
                data[key] = json.loads(v)
            except json.JSONDecodeError:
                data[key] = []
    return {"student_info": data}