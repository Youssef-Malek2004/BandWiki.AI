import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).parent.parent
CHROMA_DIR = BASE_DIR / "chroma_db"
PRIMARY_TEXT_PATH = BASE_DIR / "data"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
EMBEDDING_MODEL = "intfloat/e5-large-v2"
LLM_MODEL = "google/gemini-2.0-flash-001"
TEMPERATURE = 0.8