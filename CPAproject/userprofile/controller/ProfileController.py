from fastapi import APIRouter, UploadFile,File
from fastapi import Depends
from common.JwtCommon import get_user
from userprofile.entity.ProfileEntity import ProfileRequest
from userprofile.service.ProfileService import ProfileService
profile_router = APIRouter()

@profile_router.post("/ai_profile")
def ai_profile( profilerequest:ProfileRequest,user_id:int = Depends(get_user))->dict:
    return ProfileService.ai_pro(profilerequest.raw_text,user_id)

@profile_router.get("/query_profile")
def query_profile(user_id:int = Depends(get_user))->dict:
    return ProfileService.query_pro(user_id)

@profile_router.post("/upload_resume")
def upload_resume(file: UploadFile = File(...),user_id:int = Depends(get_user))->dict:
    return ProfileService.upload_pdf(file,user_id)

