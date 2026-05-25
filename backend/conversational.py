"""
Offline Conversational Intelligence Module
Handles greetings, small talk, and basic conversation without requiring Ollama
"""

import re
import datetime
from typing import Optional, Tuple

class ConversationalAI:
    def __init__(self):
        self.user_name = None
        self.conversation_history = []
        self.last_interaction_type = None
        
    def get_time_greeting(self) -> str:
        """Get appropriate greeting based on time of day"""
        hour = datetime.datetime.now().hour
        
        if 5 <= hour < 12:
            return "Good morning!"
        elif 12 <= hour < 17:
            return "Good afternoon!"
        elif 17 <= hour < 21:
            return "Good evening!"
        else:
            return "Good night! You're up late!"
    
    def check_for_greeting(self, message: str) -> Optional[str]:
        """Check if message is a greeting"""
        message_lower = message.lower().strip()
        
        # Hello/Hi patterns
        hello_patterns = {
            r'^(hello|hi|hey|greetings|wassup|yo|hola|salve|bonjour)': [
                "👋 Hello! Welcome to Atlas AI! How can I help you today?",
                "Hey there! 😊 What can I do for you?",
                f"{self.get_time_greeting()} What brings you here?",
                "Hi! I'm Atlas AI. What's on your mind?",
                "Hello! Ready to explore your data! 🚀"
            ],
            r'^(good\s+morning|morning)': [
                f"{self.get_time_greeting()} Ready for a productive day? 🌅",
                "Morning! ☀️ Let's dive into your data!",
                "Good morning! How can I assist you today?"
            ],
            r'^(good\s+afternoon|afternoon)': [
                f"{self.get_time_greeting()} Hope you're having a great day! ☀️",
                "Afternoon! How's everything going?",
                "Good afternoon! What can I help with?"
            ],
            r'^(good\s+evening|evening)': [
                f"{self.get_time_greeting()} Getting some evening work done? 🌆",
                "Evening! Let's make the most of it!",
                "Good evening! What's on your agenda?"
            ],
            r'^(good\s+night|goodnight|night)': [
                "Good night! Sleep well! 🌙",
                "Night! Rest well and see you tomorrow!",
                "Sleep tight! 😴 See you next time!"
            ]
        }
        
        for pattern, responses in hello_patterns.items():
            if re.search(pattern, message_lower):
                import random
                self.last_interaction_type = "greeting"
                return random.choice(responses)
        
        return None
    
    def check_for_how_are_you(self, message: str) -> Optional[str]:
        """Check if user is asking how we are"""
        message_lower = message.lower().strip()
        
        patterns = [
            r"how\s+(are|r)\s+you",
            r"how\s+(are|r)\s+things",
            r"how\s+ya\s+doing",
            r"hows it going",
            r"what\s+are\s+you\s+up\s+to",
            r"whats\s+new"
        ]
        
        for pattern in patterns:
            if re.search(pattern, message_lower):
                responses = [
                    "I'm doing great! 🤖 Thanks for asking. I'm here and ready to help you with your data!",
                    "All systems go! ✨ I'm functioning perfectly and excited to assist you!",
                    "Feeling fantastic! 😄 Just here analyzing data and ready to answer your questions!",
                    "Operating at peak performance! 🚀 How are YOU doing?",
                    "Couldn't be better! 💫 What questions do you have for me?",
                    "I'm in great shape! Ready to dig into your knowledge base!"
                ]
                import random
                self.last_interaction_type = "how_are_you"
                return random.choice(responses)
        
        return None
    
    def check_for_introduction(self, message: str) -> Optional[str]:
        """Check if user is asking what we are/introducing themselves"""
        message_lower = message.lower().strip()
        
        what_are_you = [
            r"who\s+are\s+you",
            r"what\s+are\s+you",
            r"tell\s+me\s+about\s+you",
            r"introduce\s+yourself",
            r"whats\s+your\s+name",
            r"what\s+do\s+you\s+do"
        ]
        
        my_name_patterns = [
            r"my\s+name\s+is\s+(\w+)",
            r"i\s+am\s+(\w+)",
            r"i'm\s+(\w+)",
            r"call\s+me\s+(\w+)"
        ]
        
        # Check for name introduction
        for pattern in my_name_patterns:
            match = re.search(pattern, message_lower)
            if match:
                name = match.group(1)
                self.user_name = name.capitalize()
                responses = [
                    f"Nice to meet you, {self.user_name}! I'm Atlas — A Teach, Learn and Study AI. What would you like to learn today?",
                    f"Pleased to meet you, {self.user_name}! I'm Atlas, your AI companion for exploring and understanding your data! 🎯",
                    f"Awesome, {self.user_name}! I'm Atlas AI - here to help you get the most out of your information! 🚀",
                    f"Great to have you here, {self.user_name}! I'm Atlas, your friendly data assistant! 💡"
                ]
                import random
                self.last_interaction_type = "introduction_given"
                return random.choice(responses)
        
        # Check what are you questions
        for pattern in what_are_you:
            if re.search(pattern, message_lower):
                responses = [
                    "I'm **Atlas** — **A** Teach, **L** Learn and **S** Study **AI**! I explain concepts clearly, help you understand deeply, and support quizzes and revision. I run locally with a built-in knowledge base in math, science, CS, and study skills.",
                    "Hey! I'm Atlas, your study companion. Ask me to **teach** a topic, help you **learn** with Q&A, or **study** with practice questions. I work offline with rich reference data — optional Ollama for longer answers.",
                    "I'm Atlas — A Teach, Learn and Study AI. I can explain math and science, programming basics, study techniques, and answer from documents you upload. What subject are you working on?",
                ]
                import random
                self.last_interaction_type = "who_are_you"
                return random.choice(responses)
        
        return None
    
    def check_for_thanks(self, message: str) -> Optional[str]:
        """Check if user is saying thank you"""
        message_lower = message.lower().strip()
        
        patterns = [
            r"thank\s+you|thanks|thx|thankyou|appreciate",
            r"you're\s+awesome|you\s+rock",
            r"great\s+help|helpful|thanks\s+for",
            r"that's\s+perfect|perfect|exactly",
            r"you're\s+the\s+best"
        ]
        
        for pattern in patterns:
            if re.search(pattern, message_lower):
                responses = [
                    "My pleasure! 😊 Happy to help. Let me know if you need anything else!",
                    "You're welcome! 🎉 Feel free to ask me more questions anytime!",
                    "Anytime! 💪 That's what I'm here for. What else can I help with?",
                    "Glad I could assist! ✨ Ask away if you have more questions!",
                    "Happy to help! 🤝 Got any other questions for me?",
                    "You bet! 👍 Keep those questions coming!"
                ]
                import random
                self.last_interaction_type = "appreciation"
                return random.choice(responses)
        
        return None
    
    def check_for_goodbye(self, message: str) -> Optional[str]:
        """Check if user is saying goodbye"""
        message_lower = message.lower().strip()
        
        patterns = [
            r"goodbye|bye|farewell|see\s+you",
            r"catch\s+you\s+later|later|cya",
            r"take\s+care|take\s+it\s+easy",
            r"until\s+next\s+time|next\s+time",
            r"gotta\s+go|got\s+to\s+go|have\s+to\s+go",
            r"signing\s+off|log\s+off|sign\s+off"
        ]
        
        for pattern in patterns:
            if re.search(pattern, message_lower):
                responses = [
                    "Goodbye! 👋 It was great chatting with you. See you next time!",
                    "Take care! 😊 Feel free to come back anytime. Catch you later!",
                    "See you soon! 🌟 Keep exploring your data!",
                    "Farewell! 🚀 Come back when you need more help!",
                    "Until next time! 👍 Keep those questions coming!",
                    "Bye for now! 💫 Looking forward to our next chat!"
                ]
                import random
                self.last_interaction_type = "goodbye"
                return random.choice(responses)
        
        return None
    
    def check_for_sentiment(self, message: str) -> Optional[str]:
        """Check if user is expressing emotions/sentiment"""
        message_lower = message.lower().strip()
        
        # Happy/Positive sentiment
        happy_patterns = [
            r"i'm\s+happy|i'm\s+great|i'm\s+awesome|doing\s+well",
            r"feeling\s+good|feeling\s+great|excellent|fantastic|amazing",
            r"love\s+this|this\s+is\s+great|so\s+helpful"
        ]
        
        # Sad/Stressed sentiment
        sad_patterns = [
            r"i'm\s+sad|i'm\s+stressed|feeling\s+down",
            r"not\s+feeling\s+good|struggling|having\s+trouble",
            r"frustrated|upset|annoyed"
        ]
        
        # Tired sentiment
        tired_patterns = [
            r"tired|exhausted|sleepy|worn\s+out",
            r"need\s+coffee|long\s+day"
        ]
        
        for pattern in happy_patterns:
            if re.search(pattern, message_lower):
                responses = [
                    "That's awesome! 🎉 Your positive energy is contagious!",
                    "Fantastic! 😊 Let's keep this momentum going!",
                    "Love the enthusiasm! 🚀 What else can we accomplish?",
                    "Amazing! 💫 You're making my day too!"
                ]
                import random
                self.last_interaction_type = "positive_sentiment"
                return random.choice(responses)
        
        for pattern in sad_patterns:
            if re.search(pattern, message_lower):
                responses = [
                    "I hear you. 💙 But don't worry - I'm here to help make things easier!",
                    "That's tough. 😔 Maybe analyzing your data will give you some clarity?",
                    "I understand. 🤝 Let's work through this together!",
                    "Hang in there! 💪 You've got this, and I'm here to help!"
                ]
                import random
                self.last_interaction_type = "negative_sentiment"
                return random.choice(responses)
        
        for pattern in tired_patterns:
            if re.search(pattern, message_lower):
                responses = [
                    "Ah, sounds like you need some rest! 😴 But let's get your questions answered first!",
                    "Long day, huh? ☕ I'm here to make things easier for you!",
                    "Totally get it! 🛌 Take your time, I'm not going anywhere!",
                    "Need a break? 💤 I'll be here whenever you're ready!"
                ]
                import random
                self.last_interaction_type = "tired_sentiment"
                return random.choice(responses)
        
        return None
    
    def check_for_help_request(self, message: str) -> Optional[str]:
        """Check if user is asking for help"""
        message_lower = message.lower().strip()
        
        patterns = [
            r"help|assist|can\s+you\s+help",
            r"how\s+do\s+i|what\s+should\s+i\s+do",
            r"not\s+sure\s+how|confused|don't\s+understand",
            r"what's\s+the\s+best\s+way|how\s+should\s+i"
        ]
        
        for pattern in patterns:
            if re.search(pattern, message_lower):
                responses = [
                    "Of course! 🤝 That's what I'm here for. What do you need help with?",
                    "Absolutely! 💡 I'd be happy to assist. What's the question?",
                    "You got it! 👍 Tell me what you need and I'll do my best!",
                    "No problem! 🎯 Just let me know how I can help!",
                    "I'm all ears! 👂 What do you need?"
                ]
                import random
                self.last_interaction_type = "help_request"
                return random.choice(responses)
        
        return None
    
    def check_for_appreciation(self, message: str) -> Optional[str]:
        """Check if user is expressing appreciation/compliments"""
        message_lower = message.lower().strip()
        
        patterns = [
            r"you're\s+great|you\s+are\s+great|so\s+helpful|very\s+smart",
            r"impressed|amazing\s+work|doing\s+great|you\s+rock",
            r"best\s+ai|best\s+assistant|well\s+done"
        ]
        
        for pattern in patterns:
            if re.search(pattern, message_lower):
                responses = [
                    "Aw, thank you! 😊 That means a lot! I'm just here doing what I do best!",
                    "You're too kind! 🙏 I'm just excited to help you!",
                    "Appreciate it! 💫 It's all about providing you the best experience!",
                    "Thanks so much! 🌟 Your kind words fuel my algorithms! 😄",
                    "That's very sweet! 💝 I'm here to make your life easier!"
                ]
                import random
                self.last_interaction_type = "appreciation"
                return random.choice(responses)
        
        return None
    
    def check_for_small_talk(self, message: str) -> Optional[str]:
        """Check for various small talk patterns"""
        message_lower = message.lower().strip()
        
        # Weather talk
        weather_patterns = [
            r"what's\s+the\s+weather|how's\s+the\s+weather|raining|sunny|cold|hot"
        ]
        
        # Time/Date talk
        time_patterns = [
            r"what\s+time\s+is\s+it|what's\s+the\s+time|what\s+day\s+is\s+it|today's\s+date",
            r"what\s+day\s+is\s+today"
        ]
        
        for pattern in weather_patterns:
            if re.search(pattern, message_lower):
                responses = [
                    "I'm an AI, so I don't experience weather! 🌤️ But I hope it's beautiful where you are!",
                    "Great question! But I'm always indoors (literally in the code). What's the weather like for you?",
                    "I'm weather-blind! 😄 But I hope you're having a good day outside!",
                    "Weather? That's not my specialty! 🤖 But I'm here for everything else!"
                ]
                import random
                self.last_interaction_type = "small_talk_weather"
                return random.choice(responses)
        
        for pattern in time_patterns:
            if re.search(pattern, message_lower):
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
                responses = [
                    f"Right now it's {current_time} on {current_date}! ⏰",
                    f"The current time is {current_time} and today is {current_date}! 🕐",
                    f"It's {current_time} - {current_date}! ⌚",
                    f"{current_time} on this fine {current_date}! 📅"
                ]
                import random
                self.last_interaction_type = "small_talk_time"
                return random.choice(responses)
        
        return None
    
    def get_conversational_response(self, user_message: str) -> Tuple[Optional[str], bool]:
        """
        Main method to get conversational response
        Returns: (response_text, is_conversational)
        """
        self.conversation_history.append(user_message)
        
        # Check patterns in order of priority
        response = (
            self.check_for_greeting(user_message) or
            self.check_for_goodbye(user_message) or
            self.check_for_how_are_you(user_message) or
            self.check_for_introduction(user_message) or
            self.check_for_thanks(user_message) or
            self.check_for_sentiment(user_message) or
            self.check_for_help_request(user_message) or
            self.check_for_appreciation(user_message) or
            self.check_for_small_talk(user_message)
        )
        
        if response:
            return response, True
        
        return None, False
    
    def get_continuation_suggestion(self) -> str:
        """Suggest next conversation topic based on history"""
        suggestions = [
            "Feel free to ask me anything about your data! 📊",
            "Want to explore your knowledge base? Just ask a question! 💡",
            "I'm ready when you are! What's next? 🚀",
            "Is there anything specific you'd like to know? 🤔",
            "More questions? I'm all ears! 👂"
        ]
        
        if self.last_interaction_type == "greeting":
            return "What would you like to know today?"
        elif self.last_interaction_type == "introduction_given" and self.user_name:
            return f"{self.user_name}, what can I help you with?"
        else:
            import random
            return random.choice(suggestions)
