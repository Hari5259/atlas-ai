"""
Example Conversations with Atlas AI
Demonstrating various conversational features
"""

GREETING_EXAMPLES = [
    {
        "title": "Morning Greeting",
        "exchanges": [
            ("Hello", "👋 Hello! Welcome to Atlas AI! How can I help you today?"),
            ("Good morning", "Good morning! ☀️ Ready for a productive day?"),
            ("My name is Sarah", "Nice to meet you, Sarah! 👋 I'm Atlas AI, your personal assistant...")
        ]
    },
    {
        "title": "Curious User",
        "exchanges": [
            ("Hi there", "Hey there! 😊 What can I do for you?"),
            ("Who are you?", "I'm Atlas AI - a conversational AI designed to help you..."),
            ("What time is it?", "Right now it's 02:30 PM on Thursday, May 22, 2026! ⏰"),
            ("Thanks for the info", "You're welcome! 🎉 Feel free to ask me more questions anytime!")
        ]
    },
    {
        "title": "Emotional Support",
        "exchanges": [
            ("I'm feeling stressed", "I understand. 🤝 Let's work through this together!"),
            ("But I got good news!", "That's awesome! 🎉 Your positive energy is contagious!"),
            ("You're really helpful", "Aw, thank you! 😊 That means a lot!"),
            ("Goodbye", "Take care! 😊 Feel free to come back anytime. Catch you later!")
        ]
    },
    {
        "title": "Knowledge Base Query",
        "exchanges": [
            ("Hey Atlas", "👋 Hello! Welcome to Atlas AI! How can I help you today?"),
            ("Tell me about Python", "📚 Based on 2 document(s) - Python is a high-level programming language..."),
            ("What about FastAPI?", "📚 Based on 1 document(s) - FastAPI is a modern, fast web framework..."),
            ("Thanks!", "My pleasure! 😊 Happy to help. Let me know if you need anything else!")
        ]
    },
    {
        "title": "Evening Wind Down",
        "exchanges": [
            ("Good evening", "Good evening! 🌆 Getting some evening work done?"),
            ("I'm tired today", "Totally get it! 🛌 Take your time, I'm not going anywhere!"),
            ("Good night", "Good night! Sleep well! 🌙"),
        ]
    }
]

# Test cases for conversation patterns
CONVERSATION_TEST_CASES = [
    # Greetings
    ("hello", "greeting"),
    ("hi there", "greeting"),
    ("good morning", "greeting"),
    ("good afternoon", "greeting"),
    ("good evening", "greeting"),
    ("hey", "greeting"),
    
    # How are you
    ("how are you?", "how_are_you"),
    ("how ya doing?", "how_are_you"),
    ("what's up?", "how_are_you"),
    
    # Introduction
    ("who are you?", "who_are_you"),
    ("what are you?", "who_are_you"),
    ("my name is John", "introduction_given"),
    ("I'm Alice", "introduction_given"),
    ("call me Bob", "introduction_given"),
    
    # Gratitude
    ("thanks", "appreciation"),
    ("thank you", "appreciation"),
    ("you rock", "appreciation"),
    ("you're awesome", "appreciation"),
    
    # Goodbye
    ("bye", "goodbye"),
    ("goodbye", "goodbye"),
    ("see you later", "goodbye"),
    ("catch you later", "goodbye"),
    
    # Sentiment
    ("I'm happy", "positive_sentiment"),
    ("feeling great", "positive_sentiment"),
    ("I'm sad", "negative_sentiment"),
    ("stressed out", "negative_sentiment"),
    ("tired", "tired_sentiment"),
    ("exhausted", "tired_sentiment"),
    
    # Help
    ("help", "help_request"),
    ("can you help?", "help_request"),
    ("I need help", "help_request"),
    
    # Small talk
    ("what time is it?", "small_talk_time"),
    ("what's the weather?", "small_talk_weather"),
]
