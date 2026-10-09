import smtplib
from email.mime.text import MIMEText
import random
from common import JwtCommon, RedisCommon
from user.dao import LoginDao
import os
from dotenv import load_dotenv
from user.util import EncryptUtil
load_dotenv()
from common.ResponseCommon import error,success
from userprofile.service.BaseInfoService import InfoService
class LoginService:
#登录
    @staticmethod
    def password_login(email:str,password:str)-> dict:
        result = LoginDao.verify(email)
        # 查询用户是否已经注册
        if result.get("code") != 200:
            return error("用户不存在")
        # 取出密码和输入密码进行对比
        data= result.get("data")
        hash_password = data.get("password")
        data = EncryptUtil.verify_password(password, hash_password)
        # 登录成功就发token
        if data:
            token_data = {}
            user_info = result['data']
            token_data['username'] = user_info.get('username')
            token_data['user_id'] = user_info.get('id')
            get_token =JwtCommon.create_token(token_data)
            # 判断用户信息是否已经存在
            has_profile = InfoService.query_info(
                token_data['user_id']
            )
            return success(
                data={
                    "access_token":get_token,
                    "token_type":"bearer",
                    "username":token_data['username'],
                    "has_profile": has_profile
                },
                msg="登录成功"
            )
        return error("密码错误")
    # 发送验证码
    @staticmethod
    def send_code(email:str)-> dict:
        result = LoginDao.verify(email)
        # 查询用户是否已经注册
        if result.get("code") != 200:
            return error("用户不存在")
        # 生成4位验证码
        code = random.randint(1000, 9999)
        # 配置发送信息
        sender = os.getenv("SENDER_EMAIL")  # 发送方，验证码从这里发出
        sender_pwd = os.getenv("SENDER_EMAIL_PASSWORD")  # 授权码
        subject = "这是你的验证码"  # 邮件主题
        content = f"验证码位为{code},有效期1分钟"
        username = result["data"].get("user_name")
        # 创建邮件对象
        message = MIMEText(content, "plain", "utf-8")
        # 添加内容
        message["From"] = sender
        message["To"] = email
        message["Subject"] = subject
        # 发送邮件
        try:
            # 构建发送邮件的对象
            smtp = smtplib.SMTP(
                host=os.getenv("SMTP_HOST"),
                port=int(os.getenv("SMTP_PORT")),
            )
            # 开启发送服务
            smtp.starttls()
            # 验证发送方的邮箱和授权码是否能对上
            smtp.login(sender, sender_pwd)
            # 发送邮件 ----从哪里【发送方】----到哪里【接收方】-----发送内容【邮件对象】
            smtp.sendmail(sender, email, message.as_string())
            # 发送成功后退出
            smtp.quit()

            # 验证码存入redis
            # 连接redis
            redis = RedisCommon.RedisClient.get_redis_conn()
            redis.setex(email, 60, code)
            return success(data=username,msg="发送成功")
        except Exception as e:
            print(f"邮件发送失败{e}")
            return error(f"邮件发送失败{e}")

    #验证验证码
    @staticmethod
    def check_code(email:str,code:int) ->dict:
        result = LoginDao.verify(email)
        token_data = {}
        if result.get("code") != 200:
            return error("用户不存在")
        user_info = result['data']
        token_data['username'] = user_info.get('username')
        token_data['user_id'] = user_info.get('id')
        re = RedisCommon.RedisClient.get_redis_conn()
        datas = re.get(email)
        # 判断用户信息是否已经存在
        has_profile = InfoService.query_info(
            token_data['user_id']
        )
        if datas == code:
            # 生成token并发送到前端
            access_token = JwtCommon.create_token(token_data)
            return success(
                    data={
                        "access_token":access_token,
                        "token_type":"bearer",
                        "username":token_data['username'],
                        "has_profile": has_profile
                    },
                    msg="验证成功"
                )
        if datas == None:
            return error("验证码已过期")
        return error("验证码错误")

if __name__ == '__main__':
    # re=LoginService.send_code("3131355723@qq.com")
    # print(re)
    rs = LoginService.password_login("2","3")
    print(rs)