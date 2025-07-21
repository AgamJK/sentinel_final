# gemini_emotion_classifier.py
import google.generativeai as genai
import re

genai.configure(api_key="AIzaSyACvcUKIeXnSGzRCLGgY2v2AkPnpipFr9E")

def classify_emotion_with_gemini(text):
    """
    Classify emotion using Gemini AI with fallback to keyword-based classification
    """
    # First try Gemini AI
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"What is the emotional tone of this customer message? Return only one word from: angry, frustrated, happy, grateful, confused, uncertain, neutral.\n\nMessage:\n{text}"
        
        response = model.generate_content(prompt)
        emotion = response.text.strip().lower()
        
        # Clean up the response (remove any extra text)
        emotion_words = ['angry', 'frustrated', 'happy', 'grateful', 'confused', 'uncertain', 'neutral', 'joy', 'thrilled', 'delighted', 'upset', 'disgusted', 'irritated', 'furious', 'puzzled', 'bewildered']
        for word in emotion_words:
            if word in emotion:
                return word
                
        return emotion if emotion else 'neutral'
        
    except Exception as e:
        print(f"Gemini API error: {e}")
        # Fallback to keyword-based classification
        return classify_emotion_by_keywords(text)

def classify_emotion_by_keywords(text):
    """
    Fallback keyword-based emotion classification when Gemini API is unavailable
    """
    text_lower = text.lower()
    
    # Negative/Angry keywords
    angry_keywords = [
        'angry', 'furious', 'frustrated', 'hate', 'terrible', 'awful', 'disgusting',
        'unacceptable', 'outrageous', 'livid', 'fed up', 'disgusted', 'irritated',
        'garbage', 'useless', 'worst', 'horrible', 'mad', 'pissed', 'annoyed'
    ]
    
    # Happy/Joy keywords
    happy_keywords = [
        'thank you', 'grateful', 'happy', 'excellent', 'amazing', 'wonderful',
        'fantastic', 'great', 'love', 'thrilled', 'delighted', 'pleased',
        'satisfied', 'outstanding', 'perfect', 'brilliant', 'awesome'
    ]
    
    # Confused keywords
    confused_keywords = [
        'confused', 'don\'t understand', 'unclear', 'puzzled', 'uncertain',
        'not sure', 'bewildered', 'help me understand', 'clarify', 'explain'
    ]
    
    # Count keyword matches
    angry_score = sum(1 for keyword in angry_keywords if keyword in text_lower)
    happy_score = sum(1 for keyword in happy_keywords if keyword in text_lower)
    confused_score = sum(1 for keyword in confused_keywords if keyword in text_lower)
    
    # Determine emotion based on highest score
    if angry_score > 0 and angry_score >= happy_score and angry_score >= confused_score:
        return 'angry'
    elif happy_score > 0 and happy_score >= confused_score:
        return 'happy'
    elif confused_score > 0:
        return 'confused'
    else:
        return 'neutral'
