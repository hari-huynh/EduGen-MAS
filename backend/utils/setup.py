import os
from dotenv import load_dotenv

load_dotenv()

def setup_gemini():
    os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")