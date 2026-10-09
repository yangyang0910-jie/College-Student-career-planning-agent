from pydantic import BaseModel,Field
from typing import Optional
#用户基本信息
class SaveEntity(BaseModel):
    #除了姓名其他都是选填
    name: str = Field(..., description="姓名")
    education: Optional[str] = Field(None, description="学历:大专/本科/硕士")
    major: Optional[str] = Field(None, description="专业")
    school: Optional[str] = Field(None, description="就读学校/毕业学校")
    graduation_date: Optional[str] = Field(None, description="毕业时间 YYYY-MM-DD")
    city: Optional[str] = Field(None, description="期望工作城市")
    job_direction: Optional[str] = Field(None, description="求职方向")