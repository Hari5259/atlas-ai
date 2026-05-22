"""
Response templates for conversational AI
Central repository for all response patterns
"""

GREETING_RESPONSES = {
    "hello": [
        "👋 Hello! Welcome to Atlas AI! How can I help you today?",
        "Hey there! 😊 What can I do for you?",
        "Hi! I'm Atlas AI. What's on your mind?",
        "Hello! Ready to explore your data! 🚀",
        "Welcome! Excited to assist you! ✨",
    ],
    "morning": [
        "Good morning! ☀️ Ready for a productive day?",
        "Morning! 🌅 Let's dive into your data!",
        "Good morning! How can I assist you?",
    ],
    "afternoon": [
        "Good afternoon! ☀️ Hope you're having a great day!",
        "Afternoon! How's everything going?",
        "Good afternoon! What can I help with?",
    ],
    "evening": [
        "Good evening! 🌆 Getting some evening work done?",
        "Evening! Let's make the most of it!",
        "Good evening! What's on your agenda?",
    ],
}

INTRODUCTION_RESPONSES = {
    "who_are_you": [
        "I'm Atlas AI! 🤖 I'm a conversational AI designed to help you interact with your data intelligently.",
        "Hey! I'm Atlas, your personal AI assistant! 💡",
        "I'm Atlas AI - a local, offline intelligence system! 🎯",
        "Welcome! I'm Atlas, your intelligent data companion! 🌟",
    ],
    "welcome_user": [
        "Nice to meet you, {name}! 👋 I'm Atlas AI, your personal assistant!",
        "Pleased to meet you, {name}! I'm Atlas 🎯",
        "Awesome, {name}! I'm Atlas - here to help! 💡",
        "Great to have you here, {name}! I'm your AI companion! 💫",
    ],
}

GRATITUDE_RESPONSES = {
    "thanks": [
        "My pleasure! 😊 Happy to help. Let me know if you need anything else!",
        "You're welcome! 🎉 Feel free to ask me more questions anytime!",
        "Anytime! 💪 That's what I'm here for. What else can I help with?",
        "Glad I could assist! ✨ Ask away if you have more questions!",
    ],
}

SENTIMENT_RESPONSES = {
    "positive": [
        "That's awesome! 🎉 Your positive energy is contagious!",
        "Fantastic! 😊 Let's keep this momentum going!",
        "Love the enthusiasm! 🚀 What else can we accomplish?",
        "Amazing! 💫 You're making my day too!",
    ],
    "negative": [
        "I hear you. 💙 But don't worry - I'm here to help make things easier!",
        "That's tough. 😔 Maybe analyzing your data will give you clarity?",
        "I understand. 🤝 Let's work through this together!",
        "Hang in there! 💪 You've got this, and I'm here to help!",
    ],
    "tired": [
        "Ah, sounds like you need some rest! 😴 But let's get your questions answered first!",
        "Long day, huh? ☕ I'm here to make things easier for you!",
        "Totally get it! 🛌 Take your time, I'm not going anywhere!",
        "Need a break? 💤 I'll be here whenever you're ready!",
    ],
}

FAREWELL_RESPONSES = {
    "goodbye": [
        "Goodbye! 👋 It was great chatting with you. See you next time!",
        "Take care! 😊 Feel free to come back anytime. Catch you later!",
        "See you soon! 🌟 Keep exploring your data!",
        "Farewell! 🚀 Come back when you need more help!",
    ],
}

STATUS_RESPONSES = {
    "how_are_you": [
        "I'm doing great! 🤖 Thanks for asking. I'm here and ready to help!",
        "All systems go! ✨ I'm functioning perfectly and excited to assist!",
        "Feeling fantastic! 😄 Just here and ready to answer your questions!",
        "Operating at peak performance! 🚀 How are YOU doing?",
        "I'm in great shape! Ready to dig into your knowledge base!",
    ],
}

HELP_RESPONSES = {
    "help": [
        "Of course! 🤝 That's what I'm here for. What do you need help with?",
        "Absolutely! 💡 I'd be happy to assist. What's the question?",
        "You got it! 👍 Tell me what you need and I'll do my best!",
        "No problem! 🎯 Just let me know how I can help!",
        "I'm all ears! 👂 What do you need?",
    ],
}
