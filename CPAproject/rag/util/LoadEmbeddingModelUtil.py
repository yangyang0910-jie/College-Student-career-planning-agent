#加载向量化模型
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings

_embedding_model = None
def load_embedding_model() -> HuggingFaceEmbeddings:
    # 单例缓存：避免每次请求都重新加载模型
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = HuggingFaceEmbeddings(
            model_name = os.getenv("EMBEDDING_MODEL_PATH"),
            model_kwargs={
                "device":"cpu",
                "local_files_only":True,
            },
        )
    return _embedding_model