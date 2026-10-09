from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

class LLM:
    _llm=None
    @classmethod
    def load_model(cls) -> ChatOpenAI:
        if cls._llm is None:
            cls._llm = ChatOpenAI(
                api_key=os.getenv("API_KEY"),
                base_url=os.getenv("BASE_URL"),
                model=os.getenv("MODEL_NAME"),
                streaming = True,
                temperature=0,
            )
        return cls._llm