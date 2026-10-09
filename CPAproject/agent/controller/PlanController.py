from fastapi import APIRouter
from fastapi import Depends
from agent.dao.CareerPlanDao import  list_reports, get_report, delete_report
from agent.service.PolishService import polish_report
from common.JwtCommon import get_user
plan_router = APIRouter()

# 历史报告列表
@plan_router.get("/report_list")
def report_list(user_id: int = Depends(get_user)) -> dict:
    return list_reports(user_id)
#提取报告
@plan_router.get("/report_detail")
def report_detail(report_id: int, user_id: int = Depends(get_user)) -> dict:
    return get_report(report_id, user_id)

#ai润色
@plan_router.post("/report_polish")
def polish(report_id: int, user_id: int = Depends(get_user)) -> dict:
   return polish_report(user_id, report_id)
#删除报告
@plan_router.post("/report_delete")
def report_delete(report_id: int, user_id: int = Depends(get_user)) -> dict:
   return delete_report(report_id, user_id)