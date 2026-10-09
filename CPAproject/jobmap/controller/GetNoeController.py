from fastapi import APIRouter
from jobmap.service import JobMapService

jobprofile_router = APIRouter()

@jobprofile_router.get("/job_paths")
def job_paths(job_name: str) -> dict:
    return JobMapService.get_noe(job_name)
@jobprofile_router.get("/job_list")
def get_joblist() -> dict:
    return JobMapService.get_job_name()