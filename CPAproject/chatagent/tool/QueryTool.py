from langchain_core.tools import tool
from rag.service.RetrieveService import RagService

@tool
def career_rag_search(question: str) -> str:
    """
    查询职业规划知识库。
    用于检索岗位技能要求、行业发展趋势、
    岗位成长路径、学习提升方向等职业相关知识。
    """
    try:
        docs = RagService.retrieve(question=question, candidate_k=10, top_k=5)
    except Exception as e:
        print(f"RAG检索异常: {e}")
        return "知识库暂时不可用，请稍后再试。"
    if not docs:
        return "没有检索到相关知识。"
    result = []
    for index, doc in enumerate(docs, start=1):
        job = doc.metadata.get("job", "")
        title = doc.metadata.get("title", "")
        result.append(f"知识片段{index}（岗位：{job}｜来源：{title}）\n{doc.page_content}")
    return "\n\n".join(result)

if __name__ == "__main__":
    print(career_rag_search.invoke({"question": "java 行业趋势 薪资"}))