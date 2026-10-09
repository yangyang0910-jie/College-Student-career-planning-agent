from user.dao import RegisterDao
from user.util import EncryptUtil
from common.ResponseCommon import error,success
# 注册
def register(username:str, email:str, password:str) -> dict:
    # 查询用户是否已经注册过
    result = RegisterDao.query_user(email)
    data = result["msg"]
    if data == "用户已存在":
        return error("用户已存在")
    # 给用户密码加密
    hash_password = EncryptUtil.hash_password(password)
    # 在数据库插入用户信息
    result = RegisterDao.save_user(username, email, hash_password)
    if result["code"] == 200:
        return success("注册成功")
    return error(result["code"])
if __name__ == '__main__':
    re = register("yy","3131355723@qq.com","123456")