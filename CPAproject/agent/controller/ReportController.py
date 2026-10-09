from fastapi import APIRouter
from fastapi import Depends
from starlette.responses import StreamingResponse
from collections.abc import AsyncGenerator

from common.JwtCommon import get_user
from agent.graph.CareerGraph import stream_career_graph
from common.ResponseCommon import error
from userprofile.service.BaseInfoService import InfoService
report_router = APIRouter()

@report_router.get("/generate_report")
async def generate_report(target_position: str = None, user_id: int = Depends(get_user)):
    tp = target_position
    if not tp:
        tp = (InfoService.get_info(user_id) or {}).get("job_direction")
    if not tp:
        return error("尚未设置目标岗位，请先在基础信息页填写")
    async def sse_gen() :
        async for data in stream_career_graph(user_id, tp):
            yield data
    return StreamingResponse(
        sse_gen(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
