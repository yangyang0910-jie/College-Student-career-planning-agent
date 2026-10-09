import jieba
from langchain_chroma import Chroma
from langchain_core.documents import Document
from rank_bm25 import  BM25Okapi
from rag.util import ConnDatabaseUtil

# 中文停用词表（常见停用词，避免无意义词干扰BM25排序）
STOP_WORDS = set([
    "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都",
    "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会",
    "着", "没有", "看", "好", "自己", "这", "那", "他", "她", "它", "们",
    "这个", "那个", "什么", "哪", "怎么", "吗", "呢", "吧", "啊", "哦",
    "还", "被", "把", "让", "从", "对", "与", "但", "而", "或", "所",
    "为", "以", "及", "可", "可以", "能", "能够", "应该", "需要", "已经",
    "虽然", "如果", "因为", "所以", "只是", "还是", "不过", "然后",
    "之", "其", "中", "等", "等等", "即", "使", "向", "将", "按", "当",
    "于", "由", "比", "除了", "关于", "以及", "并且", "此外", "另外",
    "过", "着", "来", "去", "做", "作", "像", "如", "如同", "由于",
])

#分词+过滤
def participle(text: str) -> list[str]:
    text_cut =jieba.cut(text)
    result = []
    for word in text_cut:
        if word.strip() not in STOP_WORDS and len(word.strip())>0:
            result.append(word)
    return  result

#创建BM检索对象
_bm25_cache = None
def bm_object(chroma_db: Chroma) -> tuple[BM25Okapi, list[Document]]:
    #取出数据库中的数据
    text=chroma_db.get()
    #处理数据格式-----和检索器一样的
    ids = text['ids']
    documents = text['documents']
    metadatas = text['metadatas']
    text =[Document(id=ids[i],page_content=documents[i],metadata=metadatas[i])for i in range(len(ids))]
    #分词
    docs=[participle(doc) for doc in documents]
    #创建BM25对象
    bm25=BM25Okapi(docs)
    return bm25,text

#BM25检索
def BM_retriever(bm25: BM25Okapi, text: list[Document], question: str, k: int = 10,
                 metadata_filter: dict | None = None) -> list[Document]:
    score = bm25.get_scores(participle(question))
    scored = [(i, s) for i, s in enumerate(score) if s > 0]  # 过滤0分，宁缺毋滥
    if metadata_filter:
        # 岗位过滤：只保留目标岗位自己的文档，防止通用词把别家文档顶进候选池
        scored = [(i, s) for i, s in scored
                  if all(text[i].metadata.get(kk) == vv for kk, vv in metadata_filter.items())]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [text[i] for i, _ in scored[:k]]

if __name__ == '__main__':
    chroma_db =ConnDatabaseUtil.chroma_conn()
    bm25,text=bm_object(chroma_db)
    BM_retriever(bm25,text,"",10)