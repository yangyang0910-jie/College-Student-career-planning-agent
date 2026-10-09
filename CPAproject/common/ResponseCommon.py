from typing import Any

def success(data: Any = None, msg: str = "成功",code: int = 200) -> dict:
    return {"code": code, "msg": msg, "data": data}

def error(msg: str = "失败", data: Any = None, code: int = 500) -> dict:
    return {"code": code, "msg": msg, "data": data}
