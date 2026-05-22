"""
Unit tests for ConversationalAI module
Tests all conversation patterns and responses
"""

import pytest
from conversational import ConversationalAI

@pytest.fixture
def ai():
    """Initialize ConversationalAI instance for testing"""
    return ConversationalAI()

class TestGreetings:
    def test_hello_greeting(self, ai):
        response, is_conv = ai.get_conversational_response("hello")
        assert is_conv == True
        assert response is not None
    
    def test_hi_greeting(self, ai):
        response, is_conv = ai.get_conversational_response("hi")
        assert is_conv == True
        assert "welcome" in response.lower() or "hello" in response.lower()
    
    def test_good_morning(self, ai):
        response, is_conv = ai.get_conversational_response("good morning")
        assert is_conv == True
        assert response is not None

class TestIntroductions:
    def test_who_are_you(self, ai):
        response, is_conv = ai.get_conversational_response("who are you?")
        assert is_conv == True
        assert "atlas" in response.lower()
    
    def test_user_name_recognition(self, ai):
        response, is_conv = ai.get_conversational_response("my name is Alice")
        assert is_conv == True
        assert "Alice" in response
        assert ai.user_name == "Alice"
    
    def test_personalized_response_with_name(self, ai):
        ai.get_conversational_response("my name is Bob")
        response, is_conv = ai.get_conversational_response("thank you")
        assert "Bob" in response or is_conv == True

class TestSentiment:
    def test_positive_sentiment(self, ai):
        response, is_conv = ai.get_conversational_response("I'm feeling great")
        assert is_conv == True
        assert response is not None
    
    def test_negative_sentiment(self, ai):
        response, is_conv = ai.get_conversational_response("I'm stressed")
        assert is_conv == True
        assert "understand" in response.lower() or "support" in response.lower()
    
    def test_tired_sentiment(self, ai):
        response, is_conv = ai.get_conversational_response("I'm exhausted")
        assert is_conv == True
        assert response is not None

class TestGratitude:
    def test_thank_you(self, ai):
        response, is_conv = ai.get_conversational_response("thank you")
        assert is_conv == True
        assert "welcome" in response.lower() or "pleasure" in response.lower()
    
    def test_thanks(self, ai):
        response, is_conv = ai.get_conversational_response("thanks")
        assert is_conv == True
        assert response is not None

class TestGoodbye:
    def test_goodbye(self, ai):
        response, is_conv = ai.get_conversational_response("goodbye")
        assert is_conv == True
        assert "see" in response.lower() or "bye" in response.lower()
    
    def test_bye(self, ai):
        response, is_conv = ai.get_conversational_response("bye")
        assert is_conv == True
        assert response is not None

class TestSmallTalk:
    def test_how_are_you(self, ai):
        response, is_conv = ai.get_conversational_response("how are you?")
        assert is_conv == True
        assert response is not None
    
    def test_time_query(self, ai):
        response, is_conv = ai.get_conversational_response("what time is it?")
        assert is_conv == True
        assert ":" in response  # Contains time format

class TestHelpRequest:
    def test_help_request(self, ai):
        response, is_conv = ai.get_conversational_response("can you help?")
        assert is_conv == True
        assert "help" in response.lower()

class TestConversationHistory:
    def test_history_tracking(self, ai):
        ai.get_conversational_response("hello")
        ai.get_conversational_response("my name is Alex")
        assert len(ai.conversation_history) == 2
        assert "hello" in ai.conversation_history[0].lower()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
