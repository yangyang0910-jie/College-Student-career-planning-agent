from fastapi import APIRouter
from fastapi import Depends
from common.JwtCommon import get_user
from common.ResponseCommon import success
from userprofile.entity.BaseInfoEntity import SaveEntity
from userprofile.service.BaseInfoService import InfoService
info_router = APIRouter()
@info_router.post("/info_save")
def save_baseinfo(saveinfoEntity: SaveEntity, user_id: int = Depends(get_user)) -> dict:
    return InfoService.save_info(saveinfoEntity, user_id)

@info_router.get("/info_query")
def get_baseinfo(user_id: int = Depends(get_user)) -> dict:
    return success(data=InfoService.get_info(user_id))

