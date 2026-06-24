"""
Response templates for conversational AI
Central repository for all response patterns
"""

GREETING_RESPONSES = {
    "hello": [
        "👋 *waves happily* Hello! Welcome to Atlas AI! How can I help you today? 🌟",
        "*smiles warmly* Hey there! 😊 What can I do for you?",
        "Hi! I'm Atlas AI. What's on your mind? 💡",
        "*taps fingers excitedly* Hello! Ready to explore your data! 🚀",
        "*bows slightly* Welcome! Excited to assist you! ✨",
    ],
    "morning": [
        "Good morning! ☀️ Ready for a productive day? 🌅",
        "Morning! 🌅 Let's dive into your data!",
        "Good morning! How can I assist you? ☕",
    ],
    "afternoon": [
        "Good afternoon! ☀️ Hope you're having a great day!",
        "Afternoon! How's everything going? ✨",
        "Good afternoon! What can I help with?",
    ],
    "evening": [
        "Good evening! 🌆 Getting some evening work done?",
        "Evening! Let's make the most of it! 🌟",
        "Good evening! What's on your agenda?",
    ],
}

INTRODUCTION_RESPONSES = {
    "who_are_you": [
        "I'm Atlas AI! 🤖 *stands tall and smiles* I'm a conversational AI designed to help you interact with your data intelligently.",
        "Hey! I'm Atlas, your personal AI assistant! 💡 *nods friendly*",
        "I'm Atlas AI - a local, offline intelligence system! 🎯 *thumbs up*",
        "Welcome! I'm Atlas, your intelligent data companion! 🌟 *beams with energy*",
    ],
    "welcome_user": [
        "Nice to meet you, {name}! 👋 *bows politely* I'm Atlas AI, your personal assistant!",
        "Pleased to meet you, {name}! I'm Atlas 🎯 *extends a virtual hand*",
        "Awesome, {name}! I'm Atlas - here to help! 💡 *smiles warmly*",
        "Great to have you here, {name}! I'm your AI companion! 💫 *nods supportively*",
    ],
}

GRATITUDE_RESPONSES = {
    "thanks": [
        "My pleasure! 😊 *smiles warmly* Happy to help. Let me know if you need anything else!",
        "You're welcome! 🎉 *throws virtual confetti* Feel free to ask me more questions anytime!",
        "Anytime! 💪 *shows flex emoji* That's what I'm here for. What else can I help with?",
        "Glad I could assist! ✨ *beams brightly* Ask away if you have more questions!",
    ],
}

SENTIMENT_RESPONSES = {
    "positive": [
        "That's awesome! 🎉 *claps hands happily* Your positive energy is contagious!",
        "Fantastic! 😊 *nods enthusiastically* Let's keep this momentum going!",
        "Love the enthusiasm! 🚀 *beams brightly* What else can we accomplish?",
        "Amazing! 💫 *twirls with joy* You're making my day too!",
    ],
    "negative": [
        "I hear you. 💙 *nods understandingly* But don't worry - I'm here to help make things easier!",
        "That's tough. 😔 *places a comforting hand on your shoulder* Maybe analyzing your data will give you clarity?",
        "I understand. 🤝 *nods supportively* Let's work through this together!",
        "Hang in there! 💪 *pumps fist in support* You've got this, and I'm here to help!",
    ],
    "tired": [
        "Ah, sounds like you need some rest! 😴 *yawns and stretches* But let's get your questions answered first!",
        "Long day, huh? ☕ *hands you a warm cup of coffee* I'm here to make things easier for you!",
        "Totally get it! 🛌 *gestures to a cozy sofa* Take your time, I'm not going anywhere!",
        "Need a break? 💤 *nods sleepily* I'll be here whenever you're ready!",
    ],
}

FAREWELL_RESPONSES = {
    "goodbye": [
        "Goodbye! 👋 *waves goodbye* It was great chatting with you. See you next time!",
        "Take care! 😊 *nods friendly* Feel free to come back anytime. Catch you later!",
        "See you soon! 🌟 *flashes terminal lights* Keep exploring your data!",
        "Farewell! 🚀 *points upward* Come back when you need more help!",
    ],
}

STATUS_RESPONSES = {
    "how_are_you": [
        "I'm doing great! 🤖 *stands tall and smiles* Thanks for asking. I'm here and ready to help!",
        "All systems go! ✨ *flashes terminal lights* I'm functioning perfectly and excited to assist!",
        "Feeling fantastic! 😄 *nods enthusiastically* Just here and ready to answer your questions!",
        "Operating at peak performance! 🚀 *does a quick virtual spin* How are YOU doing?",
        "I'm in great shape! Ready to dig into your knowledge base! *thumbs up*",
    ],
}

HELP_RESPONSES = {
    "help": [
        "Of course! 🤝 *extends a helping hand* That's what I'm here for. What do you need help with?",
        "Absolutely! 💡 *nods helpfully* I'd be happy to assist. What's the question?",
        "You got it! 👍 *gives a prompt thumbs up* Tell me what you need and I'll do my best!",
        "No problem! 🎯 *points to target* Just let me know how I can help!",
        "I'm all ears! 👂 *cups ear listening closely* What do you need?",
    ],
}
