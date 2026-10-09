from userprofile.service.BaseInfoService import InfoService
from agent.state.CareerState import CareerState

# 加载用户画像
def load_base_node(state: CareerState) -> dict:
    # 获取 user_id
    user_id = state["user_id"]
    if not user_id:
        raise ValueError("state中缺少user_id")
    # 获取用户基本信息
    user_info = InfoService.get_info(user_id)
    if not user_info:
        raise ValueError("未查询到用户基本信息")
    # 优先用 state 里传入的目标岗位；如果没有就用用户基础信息里保存的求职方向。
    target_position = state.get("target_position") or user_info.get("job_direction")
    if not target_position:
        raise ValueError("尚未设置目标岗位,请先在基础信息页填写")
    return {
        "user_info": user_info,
        "target_position": target_position
    }