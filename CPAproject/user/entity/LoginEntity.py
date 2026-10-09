from pydantic import BaseModel,Field
class PasswordEntity(BaseModel):
    email:str = Field(...,description="账号")
    password:str = Field(...,description="密码")
class CodeEntity(BaseModel):
    email:str = Field(...,description="账号")
class CheckEntity(BaseModel):
    email:str = Field(...,description="账号")
    code:str = Field(...,description="验证码")