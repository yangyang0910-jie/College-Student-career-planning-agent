import os
from dotenv import load_dotenv
from FlagEmbedding import FlagReranker
load_dotenv()
_rerank_model = None
def rerankMdel() -> FlagReranker:
    # 单例缓存：避免每次请求都重新加载模型
    global _rerank_model
    if _rerank_model is None:
        _rerank_model = FlagReranker(
            model_name_or_path=os.getenv("RERANK_MODEL_PATH"),
            # use_fp16=True,
            devices="cpu",
            model_kwargs={
                "low_cpu_mem_usage": False,  # 关键：禁用低内存模式，防止触发 meta tensor
                "local_files_only": True  # 可选：如果你确定本地有文件
            }
        )
    return _rerank_model