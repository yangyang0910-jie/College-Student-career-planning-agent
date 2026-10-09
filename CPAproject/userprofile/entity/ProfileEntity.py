from pydantic import BaseModel
class ProfileRequest(BaseModel):
    raw_text: str