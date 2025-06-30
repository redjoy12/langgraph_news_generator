import os
from dotenv import load_dotenv

load_dotenv()

# --- API KEYS ---
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
SERPER_API_KEY = os.environ.get("SERPER_API_KEY")
print(GOOGLE_API_KEY)
print(SERPER_API_KEY)
# --- MODEL SETTINGS ---
MODEL_NAME = "gemini-2.5-flash"
DEFAULT_TEMPERATURE = 0.3
MAX_TOKENS = 8192

# --- CACHING SETTINGS ---
CACHE_TTL = 3600  # 1 hour in seconds
ENABLE_CACHING = True

# --- STREAMING SETTINGS ---
ENABLE_STREAMING = True
STREAM_CHUNK_SIZE = 512

# --- CONSTANTS ---
TOPIC = "topic"
RESEARCH_REPORT = "research_report"
BLOG_POST = "blog_post"
EDITED_POST = "edited_post"
FINAL_POST = "final_post"

# --- AGENT CONFIGURATION ---
AGENT_TIMEOUT = 300  # 5 minutes
MAX_RETRIES = 3

# --- UI SETTINGS ---
PROGRESS_UPDATE_INTERVAL = 0.1  # seconds
DEFAULT_ARTICLE_LENGTH = "medium"  # short, medium, long

# --- ERROR MESSAGES ---
ERROR_MESSAGES = {
    "api_key_missing": "API keys not configured. Please check your .env file.",
    "generation_failed": "Failed to generate content. Please try again.",
    "timeout_error": "Generation took too long. Please try with a simpler topic.",
    "rate_limit": "API rate limit reached. Please wait a moment and try again."
}

# --- SUCCESS MESSAGES ---
SUCCESS_MESSAGES = {
    "cache_hit": "🚀 Found cached result! Loading instantly...",
    "generation_complete": "✅ Article generated successfully!",
    "streaming_complete": "🎉 All agents have completed their work!"
}