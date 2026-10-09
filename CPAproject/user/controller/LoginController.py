from fastapi import APIRouter
from user.service.LoginService import LoginService
from user.entity.LoginEntity import PasswordEntity,CodeEntity,CheckEntity
#创建子路由对象
login_router =APIRouter()

#密码登录
@login_router.post(
    path='/login',
    summary="登录账号",
)
def login_user(passwordentity : PasswordEntity) -> dict:
    return LoginService.password_login(passwordentity.email,passwordentity.password)
#验证码登录
#发送验证码
@login_router.post(
    path='/sendcode',
    summary="发送验证码",
)
def login_user(codeentity : CodeEntity) -> dict:
    return LoginService.send_code(codeentity.email)
#验证验证码
@login_router.post(
    path='/checkcode',
    summary="验证验证码",
)
def check_code(checkentity : CheckEntity) -> dict:
    return LoginService.check_code(checkentity.email,checkentity.code)