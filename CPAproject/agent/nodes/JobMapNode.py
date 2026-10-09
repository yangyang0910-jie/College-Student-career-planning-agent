from agent.state.CareerState import CareerState
from jobmap.service.JobMapService import get_noe
# 加载目标岗位的晋升和换岗路径
def load_job_map_node(state: CareerState) -> dict:
    # 获取目标岗位
    target_position = state.get("target_position")
    if not target_position:
        raise ValueError("state中缺少target_position")
    # 查询岗位晋升和换岗路径
    paths = get_noe(target_position)
    return {"paths": paths}