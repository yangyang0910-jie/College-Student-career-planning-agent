import asyncio
import json
import uuid
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from chatagent.graph.ChatGraph import stream as chat_stream
from chatagent.memory.SimpleMemory import SimpleMemory
from chatagent.memory.MemoryUpdate import update_memory
from common.JwtCommon import get_user
from common.ModelCommon import LLM
from common.ResponseCommon import success
chat_router = APIRouter()

@chat_router.get("/chat")
async def chat(question: str, sessionId: str = "", user_id: int = Depends(get_user)):
    session_id = sessionId or f"chat_{user_id}_{uuid.uuid4().hex[:8]}"
    async def sse():
        full  = []
        async for chunk in chat_stream(question, user_id, session_id):
            if chunk.get("delta"):
                full.append(chunk["delta"])
                yield f"data: {json.dumps({'content': chunk['delta']}, ensure_ascii=False)}\n\n"
            if chunk.get("error"):
                yield f"data: {json.dumps({'content': f'[出错:{chunk["error"]}]'})}\n\n"
            if chunk.get("done"):
                answer = "".join(full)
                # 异步存入四层记忆
                asyncio.create_task(save_memory(user_id, session_id,question, answer))
                yield f"data: {json.dumps({'content': '[done]'})}\n\n"
    return StreamingResponse(sse(), media_type="text/event-stream", headers={"Cache-Control": "no-cache","X-Accel-Buffering": "no"})

#四层记忆更新
async def save_memory(user_id: int, session_id: str, question: str, answer: str):
    memory = SimpleMemory(user_id, session_id)
    memory.add_window("user", question)
    memory.add_window("assistant", answer)
    #更新记忆
    await asyncio.to_thread(update_memory, memory, LLM.load_model(),question, answer)

#对话历史
@chat_router.post("/saveConversation")
def save_conversation(data: dict, user_id: int = Depends(get_user)) -> dict:
    from chatagent.dao.HistoryDao import save
    rid = save(data.get("sessionId") or "", user_id,
               data.get("question") or "", data.get("answer") or "")
    return success(data=rid)


@chat_router.get("/historyMenu")
def history_menu(user_id: int = Depends(get_user)) -> dict:
    from chatagent.dao.HistoryDao import history_list
    return success(data=history_list(user_id))


@chat_router.get("/queryOneHistory")
def query_one(sessionId: str, user_id: int = Depends(get_user)) -> dict:
    from chatagent.dao.HistoryDao import get_conversation
    return success(data=get_conversation(user_id, sessionId))


@chat_router.get("/deleteOneHistory")
def delete(sessionId: str, user_id: int = Depends(get_user)) -> dict:
    from chatagent.dao.HistoryDao import delete_session
    delete_session(user_id, sessionId)
    return success("删除成功")