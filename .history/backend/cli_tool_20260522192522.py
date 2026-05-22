#!/usr/bin/env python3
"""
Atlas AI Conversational CLI Tool
Test conversational features directly from command line
"""

import sys
from conversational import ConversationalAI

def print_banner():
    """Print Atlas AI banner"""
    print("\n" + "="*60)
    print("  🤖 ATLAS AI - Conversational AI CLI Tool")
    print("="*60)
    print("\nType your message and press Enter.")
    print("Commands: 'quit' or 'exit' to end conversation\n")

def print_response_info(response_type, user_name=None):
    """Print response metadata"""
    if response_type == "greeting":
        print("  [Type: Greeting Response]")
    elif response_type == "how_are_you":
        print("  [Type: Status Check]")
    elif response_type == "introduction_given":
        print(f"  [Type: Name Stored - {user_name}]")
    elif response_type == "who_are_you":
        print("  [Type: Self-Introduction]")
    elif response_type == "appreciation":
        print("  [Type: Gratitude Response]")
    elif response_type == "goodbye":
        print("  [Type: Farewell]")
    elif response_type == "positive_sentiment":
        print("  [Type: Positive Sentiment]")
    elif response_type == "negative_sentiment":
        print("  [Type: Negative Sentiment]")
    elif response_type == "help_request":
        print("  [Type: Help Request]")

def format_response(response):
    """Format response for display"""
    return f"\nAtlas AI: {response}\n"

def main():
    """Main CLI loop"""
    print_banner()
    
    ai = ConversationalAI()
    message_count = 0
    
    try:
        while True:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print(format_response("Goodbye! Thanks for chatting with me! 👋"))
                print("="*60 + "\n")
                break
            
            # Get conversational response
            response, is_conversational = ai.get_conversational_response(user_input)
            
            if is_conversational:
                print(format_response(response))
                print(f"  [Response Type: {ai.last_interaction_type or 'general'}]")
                if ai.user_name:
                    print(f"  [User: {ai.user_name}]")
            else:
                print(format_response("(Not a conversational pattern - would use knowledge base or Ollama)"))
                print("  [Response Type: Knowledge-Based Query Required]")
            
            message_count += 1
            
    except KeyboardInterrupt:
        print("\n\nConversation ended. Goodbye! 👋")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
    
    # Print session stats
    print(f"Total messages: {message_count}")
    print(f"Conversation history length: {len(ai.conversation_history)}")
    if ai.user_name:
        print(f"User name remembered: {ai.user_name}")

if __name__ == "__main__":
    main()
