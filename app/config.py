import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration (Together AI - Free Tier)
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4000"))

# Skill Proficiency Levels
PROFICIENCY_LEVELS = ["beginner", "intermediate", "advanced", "expert"]

# Learning Path Priorities
PRIORITY_WEIGHTS = {
    "critical_gap": 0.40,
    "important_gap": 0.30,
    "nice_to_have": 0.20,
    "career_growth": 0.10,
}

# Thresholds
MIN_PROFICIENCY_FOR_ROLE = "intermediate"  # Minimum expected level for a target role
LEARNING_PATH_MAX_ITEMS = 10  # Max courses/resources per learning path
