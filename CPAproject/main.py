from fastapi import FastAPI
from chatagent.controller.ChatController import chat_router
from agent.controller.PlanController import plan_router
from agent.controller.ReportController import report_router
from user.controller.RegisterController import register_router
from user.controller.LoginController import login_router
from userprofile.controller.BaseInfoController import info_router
from userprofile.controller.ProfileController import profile_router
from jobmap.controller.GetNoeController import jobprofile_router
app = FastAPI()

# #强制 UTF-8 输出
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gbk', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='gbk', errors='replace')
# 跨域配置
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # 允许得域名 ----- 完整的客户端域名
    allow_credentials=True,  # 允许携带的cookie
    allow_methods=['*'],  # 允许请求的方法
    allow_headers=['Authorization', 'Content-Type', 'Accept'],  # 允许的请求头
)

# 注册子路由
app.include_router(
    router=register_router,
    prefix="/user",
    tags=["user"]
)

app.include_router(
    router=login_router,
    prefix="/user",
    tags=["user"]
)
app.include_router(
    router=info_router,
    prefix="/info",
    tags=["information"]
)
app.include_router(
    router=profile_router,
    prefix="/profile",
    tags=["information"]
)
app.include_router(
    router=jobprofile_router,
    prefix="/jobprofile",
    tags=["information"]
)
app.include_router(
    router=plan_router,
    prefix="/careerplan",
    tags=["career"]
)
app.include_router(
    router=report_router,
    prefix="/reportplan",
    tags=["career"]
)

app.include_router(
    router = chat_router,
    prefix="/chat",
    tags=["chat"])




# 启动服务
if __name__ == '__main__':
    # 导入uvicorn包来写命令启动fastapi服务器项目
    import uvicorn as uv
    # 配置启动
    uv.run(
    # 启动项目的文件，即FastAPI()对象所在的文件
    app="main:app",  # 配置启动的项目文件 --- mαin.py中的αpp对象
    host="localhost",  # 配置启动的服务器地址
    port=8000,  # 配置启动的服务器端口
    reload=False,  #配置关闭自动重启
)
