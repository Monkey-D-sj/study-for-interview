from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv()

teacher_model = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_API_BASE"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.5
)
