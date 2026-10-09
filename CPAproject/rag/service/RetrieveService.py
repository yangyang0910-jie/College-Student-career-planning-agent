from langchain_core.documents import Document
from rag.util import ConnDatabaseUtil
from rag.util import BM25Util
from rag.util import RRFUtile
from rag.util import RerankModelUtil
class RagService:
    @staticmethod
    def retrieve(question: str,candidate_k: int = 10,top_k: int = 5,metadata_filter: dict | None = None)-> list[Document]:
        if not question or not question.strip():
            raise ValueError("RAG检索问题不能为空")
        question = question.strip()
        try:
            chroma_db = ConnDatabaseUtil.chroma_conn()
            if chroma_db is None:
                raise RuntimeError("Chroma向量数据库连接失败")

            print("========== 向量检索 ==========")
            vector_result = chroma_db.similarity_search(question, k=candidate_k, filter=metadata_filter)
            print(f"向量检索完成，共 {len(vector_result)} 条")

            print("========== BM25检索 ==========")
            bm25, text = BM25Util.bm_object(chroma_db)
            bm_result = BM25Util.BM_retriever(bm25, text, question, candidate_k,metadata_filter)
            print(f"BM25检索完成，共 {len(bm_result)} 条")

            print("========== RRF融合 ==========")
            rrf_result = RRFUtile.RRF_fuse(bm_result,vector_result)
            print(f"RRF融合完成，共 {len(rrf_result)} 条")
            if not rrf_result:
                print("RRF融合后没有结果")
                return []
            # 去重
            docs = []
            seen = set()
            for doc in rrf_result:
                doc_id = getattr(doc, "id", None)
                if doc_id:
                    key = str(doc_id)
                else:
                    key = doc.page_content.strip()
                if key in seen:
                    continue
                seen.add(key)
                docs.append(doc)
            rrf_result = docs
            print(f"去重后，共 {len(rrf_result)} 条")

            print("========== Rerank重排序 ==========")
            reranker = RerankModelUtil.rerankMdel()
            scores = reranker.compute_score([(question, doc.page_content) for doc in rrf_result])
            print("Rerank评分：",scores)
            # Document + Score
            scored_docs = []
            for index, score in enumerate(scores):
                try:
                    score = float(score)
                except (TypeError, ValueError):
                    score = 0.0
                scored_docs.append(( rrf_result[index],score))
            # 按分数从高到低排序
                scored_docs.sort(key=lambda item: item[1],reverse=True)
            # 最终Top-K
            final_docs = [doc for doc, score in scored_docs[:top_k]]
            print(f"最终RAG结果：{len(final_docs)} 条")
            return final_docs
        except Exception as e:
            raise RuntimeError(f"RAG检索失败: {e}") from e