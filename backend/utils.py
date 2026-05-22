"""
Utility functions for Atlas AI
"""

import datetime
import re
from typing import List, Optional

def get_current_time_formatted() -> str:
    """Get current time in formatted string"""
    return datetime.datetime.now().strftime("%I:%M %p")

def get_current_date_formatted() -> str:
    """Get current date in formatted string"""
    return datetime.datetime.now().strftime("%A, %B %d, %Y")

def get_time_of_day() -> str:
    """Get time of day (morning, afternoon, evening, night)"""
    hour = datetime.datetime.now().hour
    
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    else:
        return "night"

def sanitize_input(text: str) -> str:
    """Sanitize user input"""
    return text.strip().lower()

def extract_name_from_message(message: str) -> Optional[str]:
    """Extract name from introduction patterns"""
    patterns = [
        r"my\s+name\s+is\s+(\w+)",
        r"i\s+am\s+(\w+)",
        r"i'm\s+(\w+)",
        r"call\s+me\s+(\w+)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, message.lower())
        if match:
            return match.group(1).capitalize()
    
    return None

def calculate_response_time(start_time: float, end_time: float) -> float:
    """Calculate response time in milliseconds"""
    return (end_time - start_time) * 1000

def truncate_text(text: str, max_length: int = 200) -> str:
    """Truncate text to max length with ellipsis"""
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

def has_emoji(text: str) -> bool:
    """Check if text contains emoji"""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "]+",
        flags=re.UNICODE,
    )
    return bool(emoji_pattern.search(text))

def add_emoji_to_response(response: str, emoji: str = "✨") -> str:
    """Add emoji to response if not already present"""
    if has_emoji(response):
        return response
    return f"{response} {emoji}"

def batch_messages(messages: List[str], batch_size: int = 10) -> List[List[str]]:
    """Batch messages for processing"""
    return [messages[i:i + batch_size] for i in range(0, len(messages), batch_size)]
