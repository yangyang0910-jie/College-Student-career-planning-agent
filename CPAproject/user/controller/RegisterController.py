from fastapi import APIRouter
from user.service.RegisterService import register
from user.entity.RegisterEntity import RegisterEntity
#创建子路由对象
register_router =APIRouter()

@register_router.post(
    path='/register',
    summary="注册账号",
)
def register_user(registerentity : RegisterEntity) -> dict:
    return register(registerentity.username,registerentity.email,registerentity.password)