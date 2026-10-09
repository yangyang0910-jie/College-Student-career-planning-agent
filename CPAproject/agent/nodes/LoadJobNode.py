from agent.state.CareerState import CareerState
from jobprofile.service.JobProfileService import query_profile
from jobprofile.dao.saveJobDao import SaveJobProfileDao

# 加载岗位画像
def load_job_node(state: CareerState) -> dict:
    # 获取目标岗位
    target_position = state.get("target_position")
    if not target_position:
        raise ValueError("state中缺少target_position")
    # 查询岗位画像
    job_info = query_profile(target_position)
    if not job_info:
        raise ValueError(f"岗位画像不存在：{target_position}")
    # 查询岗位市场数据
    market_stats = SaveJobProfileDao.get_market_stats(target_position)
    return {"job_info": job_info, "market_stats": market_stats, }