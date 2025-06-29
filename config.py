import os
from dotenv import load_dotenv

load_dotenv()

# --- API KEYS ---
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
SERPER_API_KEY = os.environ.get("SERPER_API_KEY")

# --- SETTINGS ---
MODEL_NAME = "gemini-2.5-flash"

# --- CONSTANTS ---
TOPIC = "topic"
RESEARCH_REPORT = "research_report"
BLOG_POST = "blog_post"