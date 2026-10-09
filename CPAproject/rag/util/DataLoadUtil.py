import os
import re
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from rag.util import LoadEmbeddingModelUtil

# 数据存储位置
all_path = Path(r"D:\workspace\CPAproject\datasets")
# 向量数据库存储位置
vector_db_path = r"D:\workspace\CPAproject\chroma_career"
# 集合名称
collection_name = "career_kb"
GENERIC_PREFIX = {"应届生", "计算机行业", "职业转型"}
# 进行数据过滤
def clean_text(text: str) -> str:
    # 轻度清洗：LLM残留/乱码/空行
    text = re.sub(r"^```(?:markdown|md)?\s*\n?", "", text)
    text = re.sub(r"\n?```\s*$", "", text)
    text = re.sub(r"^(?:好的|以下是|以下为|当然，|当然)[^\n]{0,60}\n", "", text)
    text = re.sub(r"[\uE000-\uF8FF\u0000-\u0008\u000b-\u001f]", "", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def data_load() -> None:
    # 加载数据
    all_data = []
    try:
        loader = DirectoryLoader(
            path=all_path,
            loader_cls=TextLoader,
            glob="*.md",
            loader_kwargs={"encoding": "utf-8"},
        )
        all_data = loader.load()
        print(f"成功加载 {len(all_data)} 篇")
    except Exception as e:
        print(f"加载失败: {e}")
        return
    if not all_data:
        return

    # 清洗
    # 元数据标注：剥掉已知的角度后缀，剩下的就是岗位前缀
    SUFFIXES = ("行业趋势", "社会需求", "成长路径")
    JOB_MAP = {
        "C语言": "C/C++",
        "产品专员或助理": "产品专员/助理",
        "质量管理或测试": "质量管理/测试",
        "管培生或储备干部": "管培生/储备干部",
    }
    for d in all_data:
        d.page_content = clean_text(d.page_content)
        fname = os.path.basename(d.metadata.get("source", ""))
        stem = fname.replace(".md", "")  # C语言行业趋势

        # ★ 剥后缀： endsWith哪个就剥哪个
        prefix = stem
        for suf in SUFFIXES:
            if stem.endswith(suf):
                prefix = stem[: -len(suf)]  # C语言
                break

        # 映射回图谱标准名
        d.metadata["job"] = JOB_MAP.get(prefix, prefix)  # C/C++
        d.metadata["title"] = fname
        d.metadata["generic"] = "1" if prefix in GENERIC_PREFIX else "0"
    all_data = [d for d in all_data if len(d.page_content) >= 100]
    print(f"清洗后有效: {len(all_data)} 篇")

    # 切分
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=80,
        separators=["\n## ", "\n\n### ", "\n\n", "\n", "。", "，", "｜"],
    )
    chunks = splitter.split_documents(all_data)
    print(f"切分: {len(chunks)} 块")

    # 存入数据库（结构照旧）
    embedding = LoadEmbeddingModelUtil.load_embedding_model()
    try:
        Chroma.from_documents(
            documents=chunks,
            embedding=embedding,
            collection_name=collection_name,
            persist_directory=vector_db_path,
            collection_metadata={"hnsw:space": "cosine"},
        )
        print("数据存入成功")
    except Exception as e:
        print(f"数据存放失败:{e}")
        return

if __name__ == "__main__":
    data_load()