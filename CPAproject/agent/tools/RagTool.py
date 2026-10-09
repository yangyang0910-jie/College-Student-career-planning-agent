from langchain_core.tools import tool
from rag.service.RetrieveService import RagService


@tool
def job_rag_search(question: str, job_name: str = "") -> str:
    """
    按岗位检索职业规划知识库（行业趋势/社会需求/技能提升方向/学习路线）
    优先限定在目标岗位自己的知识文档里检索，检索不到再退回全库检索，
    返回拼接好的知识片段文本。
    """
    if job_name:
        docs = RagService.retrieve(question, metadata_filter={"job": job_name})
        if not docs:  # 该岗位自己的文档里没检索到，退回全库
            docs = RagService.retrieve(question)
    else:
        docs = RagService.retrieve(question)
    if not docs:
        return f"知识库中暂无{job_name}相关资料，本章节基于通用知识生成。"
    result = []
    for d in docs:
        job = d.metadata.get('job', '')
        title = d.metadata.get('title', '')
        piece = f"【{job} {title}】\n{d.page_content}"
        result.append(piece)
    return "\n\n".join(result)
