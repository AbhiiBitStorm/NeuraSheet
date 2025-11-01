import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Model settings
MODEL_PATH = BASE_DIR / "models" / "mistral-7b-instruct-v0.2.Q4_K_M.gguf"

# LLM Configuration
LLM_CONFIG = {
    "model_path": str(MODEL_PATH),
    "n_ctx": 4096,              # Context window
    "n_threads": 4,             # CPU threads (apne system ke hisab se adjust karo)
    "n_batch": 512,             # Batch size
    "temperature": 0.1,         # Low temp = more accurate
    "max_tokens": 1024,         # Response length
    "top_p": 0.9,
    "verbose": False
}

# Paths
TOOLS_DIR = BASE_DIR / "tools"
TEST_FILES_DIR = BASE_DIR / "test_files"
OUTPUT_DIR = BASE_DIR / "output"

# Create output folder if not exists
OUTPUT_DIR.mkdir(exist_ok=True)

print("✅ Config loaded successfully!")