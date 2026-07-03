import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing in the environment.")
