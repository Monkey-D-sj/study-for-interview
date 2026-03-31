from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
import os

load_dotenv()

def get_teacher_model():
    return ChatDeepSeek(
        model="deepseek-chat",
        base_url=os.getenv("DEEPSEEK_API_BASE"),
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        temperature=0.5
    )
