from langchain_chroma import Chroma
from dotenv import load_dotenv
import  os
from rag.util import LoadEmbeddingModelUtil
load_dotenv()
def chroma_conn() -> Chroma:
    return Chroma(
        collection_name= os.getenv('COLLECTION_NAME'),
        embedding_function=LoadEmbeddingModelUtil.load_embedding_model(),
        persist_directory=os.getenv('CHROMA_PATH'),
    )