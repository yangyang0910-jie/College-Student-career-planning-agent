from typing import Literal
from pydantic import BaseModel, Field

class IntentSchema(BaseModel):
    intent: Literal["knowledge", "mine", "chat"] = Field(
        description="knowledge行业知识问答 / mine涉及用户自身画像、技能、匹配度的问题 / chat闲聊或需引导到报告的问题")
